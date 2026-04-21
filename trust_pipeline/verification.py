import requests
import re
import ssl
import socket
from urllib.parse import urlparse
from difflib import SequenceMatcher
from trust_pipeline.config import REQUEST_TIMEOUT

SHORTENERS = [
    'tinyurl.com', 'bit.ly', 't.co', 'cutt.ly', 'rb.gy',
    'is.gd', 'shorturl.at', 'rebrand.ly', 'tiny.cc', 'ow.ly'
]

# Known legitimate brands and their ONLY official domains
KNOWN_BRANDS = {
    "amazon":    ["amazon.com", "amazon.in", "amazon.co.uk", "amazon.de", "amazon.ca", "amazon.com.au"],
    "flipkart":  ["flipkart.com"],
    "google":    ["google.com", "google.co.in", "google.co.uk", "googleapis.com", "youtube.com"],
    "paypal":    ["paypal.com", "paypal.me"],
    "apple":     ["apple.com", "icloud.com", "itunes.com"],
    "netflix":   ["netflix.com"],
    "microsoft": ["microsoft.com", "live.com", "outlook.com", "office.com", "azure.com"],
    "facebook":  ["facebook.com", "fb.com", "instagram.com", "whatsapp.com", "meta.com"],
    "instagram": ["instagram.com"],
    "twitter":   ["twitter.com", "x.com"],
    "ebay":      ["ebay.com", "ebay.in", "ebay.co.uk"],
    "linkedin":  ["linkedin.com"],
}

ALL_OFFICIAL_DOMAINS = {d for domains in KNOWN_BRANDS.values() for d in domains}

# Words in a domain name that are inherently suspicious
SCAM_DOMAIN_KEYWORDS = [
    "secure", "update", "verify", "alert", "login", "account", "confirm",
    "reward", "cashback", "bonus", "claim", "refund", "kyc", "billing",
    "payment", "wallet", "identity", "parcel", "delivery", "shipment",
    "sim", "tax", "benefit", "portal", "upgrade", "mail", "subscription",
    "fix", "check", "review", "notice", "warning", "urgent", "fee",
    "support", "helpdesk", "service", "center", "centre"
]


def _similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def _detect_brand_impersonation(domain):
    domain_name = domain.split('.')[0].lower()
    for brand, official_list in KNOWN_BRANDS.items():
        if domain in official_list:
            return brand, True
        if brand in domain.lower():
            return brand, False
        if _similarity(domain_name, brand) > 0.82 and domain not in official_list:
            return brand, False
    return None, None


def _count_scam_keywords_in_domain(domain):
    """Count how many scam-related words appear in the domain name itself."""
    domain_lower = domain.lower().replace("-", " ").replace(".", " ")
    return [kw for kw in SCAM_DOMAIN_KEYWORDS if kw in domain_lower]


def internet_verify_official(user_input, domain=None):
    findings = []
    status = "UNKNOWN"
    trust_score = 50
    is_official = False

    if not domain:
        return {
            "status": status, "trust_score": trust_score,
            "message": "No domain provided for verification.",
            "findings": findings, "is_official": is_official,
            "source": "internet_verification"
        }

    # Known official domain — trust immediately
    if domain in ALL_OFFICIAL_DOMAINS:
        return {
            "status": "SAFE", "trust_score": 98,
            "message": "Domain is a verified official website.",
            "findings": ["Domain matched known official brand registry."],
            "is_official": True, "source": "internet_verification"
        }

    fetch_url = "https://" + domain
    positive_signals = 0
    negative_signals = 0

    try:
        resp = requests.get(
            fetch_url, timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            allow_redirects=True, verify=True
        )

        findings.append(f"Site responded with HTTP {resp.status_code}.")

        if resp.status_code == 200:
            positive_signals += 2
        elif resp.status_code in (301, 302, 307, 308):
            positive_signals += 1
        elif resp.status_code >= 400:
            negative_signals += 2
            findings.append(f"Site returned error status {resp.status_code}.")

        # SSL valid
        positive_signals += 2
        findings.append("Valid SSL/TLS certificate confirmed.")

        html = resp.text[:15000].lower()
        title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else ""

        if title:
            findings.append(f"Page title: \"{title[:80]}\"")
            domain_name = domain.split('.')[0]
            if domain_name in title.lower():
                positive_signals += 2
                findings.append("Page title matches domain name.")

        trust_markers = ["privacy policy", "terms of service", "terms and conditions",
                         "contact us", "about us", "©", "copyright"]
        found_markers = [m for m in trust_markers if m in html]
        if len(found_markers) >= 2:
            positive_signals += 2
            findings.append(f"Site has standard trust markers ({len(found_markers)} found).")
        elif len(found_markers) == 1:
            positive_signals += 1

        final_domain = urlparse(resp.url).netloc.lower().replace("www.", "")
        if final_domain and final_domain != domain:
            negative_signals += 1
            findings.append(f"Site redirected to a different domain: {final_domain}.")

        if len(resp.text.strip()) < 500:
            negative_signals += 2
            findings.append("Page has very little content (possible placeholder or scam page).")

    except requests.exceptions.SSLError:
        negative_signals += 3
        findings.append("SSL certificate is invalid or self-signed.")
    except requests.exceptions.ConnectionError:
        negative_signals += 4
        findings.append("Domain does not resolve or refused connection (likely non-existent).")
    except requests.exceptions.Timeout:
        negative_signals += 1
        findings.append("Site took too long to respond.")
    except Exception as e:
        negative_signals += 1
        findings.append(f"Unexpected error during live check: {str(e)[:80]}")

    net = positive_signals - negative_signals

    if net >= 4:
        status = "SAFE"
        trust_score = 85
        is_official = True
        message = "Live verification passed. Site appears legitimate."
    elif net >= 1:
        status = "LIKELY_SAFE"
        trust_score = 68
        is_official = True
        message = "Site shows signs of legitimacy but could not be fully verified."
    elif net == 0:
        status = "SUSPICIOUS"
        trust_score = 45
        message = "Verification inconclusive. Proceed with caution."
    else:
        status = "FAKE"
        trust_score = 15
        message = "Live verification failed. Site shows strong signs of being fake or malicious."

    return {
        "status": status, "trust_score": trust_score, "message": message,
        "findings": findings, "is_official": is_official, "source": "internet_verification"
    }


def analyze_url_rules(domain, normalized_url):
    findings = []
    deductions = 0
    is_shortened = False

    if not domain:
        return {"risk_score": 0, "findings": findings, "is_shortened": False}

    # 1. Shortener
    if domain.lower() in SHORTENERS:
        is_shortened = True
        deductions += 40
        findings.append("Shortened URL detected — destination is hidden.")

    # 2. Brand impersonation / typosquat
    brand, is_official_brand = _detect_brand_impersonation(domain)
    if brand and not is_official_brand:
        deductions += 60
        findings.append(f"Possible impersonation of '{brand}' — this is NOT the official domain.")
    elif brand and is_official_brand:
        findings.append(f"Domain is the official '{brand}' website.")

    if not is_official_brand:
        from trust_pipeline.utils import ensure_scheme
        full_url = ensure_scheme(normalized_url)
        parsed = urlparse(full_url)
        path = parsed.path.lower()
        query = parsed.query.lower()

        # 3. Scam keywords IN the domain name itself
        domain_scam_words = _count_scam_keywords_in_domain(domain)
        if len(domain_scam_words) >= 2:
            deductions += 50
            findings.append(f"Domain name contains multiple scam-related words: {', '.join(domain_scam_words)}.")
        elif len(domain_scam_words) == 1:
            deductions += 25
            findings.append(f"Domain name contains a suspicious keyword: '{domain_scam_words[0]}'.")

        # 4. Deceptive path segments
        deceptive_paths = ["verify", "login", "account", "secure", "update", "billing",
                           "payment", "confirm", "kyc", "refund", "claim", "reward"]
        for pattern in deceptive_paths:
            if f"/{pattern}" in path:
                deductions += 18
                findings.append(f"Suspicious path segment: '/{pattern}'.")
            if f"{pattern}=" in query:
                deductions += 12
                findings.append(f"Sensitive query parameter: '{pattern}='.")

        # 5. Excessive hyphens
        if domain.count("-") >= 2:
            deductions += 20
            findings.append("Domain has multiple hyphens (common in scam/phishing domains).")
        elif domain.count("-") == 1:
            deductions += 8
            findings.append("Domain contains a hyphen (minor risk indicator).")

        # 6. Long randomised path
        if len(path) > 60 and sum(c.isdigit() for c in path) > 5:
            deductions += 10
            findings.append("Excessively long randomised path (common in phishing links).")

        # 7. Raw IP address
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain):
            deductions += 50
            findings.append("URL uses a raw IP address instead of a domain name.")

        # 8. Brand in subdomain (paypal.com.evil.net)
        parts = domain.split(".")
        if len(parts) > 3:
            subdomain = ".".join(parts[:-2])
            for brand_name in KNOWN_BRANDS:
                if brand_name in subdomain:
                    deductions += 55
                    findings.append(f"Brand name '{brand_name}' found in subdomain — classic phishing pattern.")
                    break

        # 9. Suspicious TLD combinations with scam keywords
        tld = domain.split(".")[-1].lower()
        suspicious_tlds = ["xyz", "top", "click", "loan", "work", "gq", "tk", "ml", "cf", "ga"]
        if tld in suspicious_tlds and domain_scam_words:
            deductions += 20
            findings.append(f"Suspicious TLD '.{tld}' combined with scam keywords.")

    return {
        "risk_score": deductions,
        "findings": findings,
        "is_shortened": is_shortened
    }

SHORTENERS = [
    'tinyurl.com', 'bit.ly', 't.co', 'cutt.ly', 'rb.gy',
    'is.gd', 'shorturl.at', 'rebrand.ly', 'tiny.cc', 'ow.ly'
]

# Known legitimate brands and their ONLY official domains
KNOWN_BRANDS = {
    "amazon":    ["amazon.com", "amazon.in", "amazon.co.uk", "amazon.de", "amazon.ca", "amazon.com.au"],
    "flipkart":  ["flipkart.com"],
    "google":    ["google.com", "google.co.in", "google.co.uk", "googleapis.com", "youtube.com"],
    "paypal":    ["paypal.com", "paypal.me"],
    "apple":     ["apple.com", "icloud.com", "itunes.com"],
    "netflix":   ["netflix.com"],
    "microsoft": ["microsoft.com", "live.com", "outlook.com", "office.com", "azure.com"],
    "facebook":  ["facebook.com", "fb.com", "instagram.com", "whatsapp.com", "meta.com"],
    "instagram": ["instagram.com"],
    "twitter":   ["twitter.com", "x.com"],
    "ebay":      ["ebay.com", "ebay.in", "ebay.co.uk"],
    "linkedin":  ["linkedin.com"],
}

# Flat set of all official domains for fast lookup
ALL_OFFICIAL_DOMAINS = {d for domains in KNOWN_BRANDS.values() for d in domains}


def _check_ssl(domain):
    """Returns True if domain has a valid SSL certificate."""
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(4)
            s.connect((domain, 443))
        return True
    except Exception:
        return False


def _similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def _detect_brand_impersonation(domain):
    """
    Returns (brand, is_official) tuple.
    Catches both substring matches (amazon-login.com) and
    typosquats (amaz0n.com, arnazon.com) via similarity.
    """
    domain_name = domain.split('.')[0].lower()  # e.g. "amazon" from "amazon.com"

    for brand, official_list in KNOWN_BRANDS.items():
        # Exact official domain — no impersonation
        if domain in official_list:
            return brand, True

        # Substring match: amazon-secure.net, secure-amazon.net
        if brand in domain.lower():
            return brand, False

        # Typosquat: amzon.com, arnazon.com (similarity > 0.82)
        if _similarity(domain_name, brand) > 0.82 and domain not in official_list:
            return brand, False

    return None, None


def internet_verify_official(user_input, domain=None):
    """
    Real-time live verification of a domain.
    Checks: DNS resolution, HTTPS/SSL, HTTP status, page title,
    brand match, and redirect behaviour.
    Does NOT penalise sites for having normal e-commerce words.
    """
    findings = []
    status = "UNKNOWN"
    trust_score = 50
    is_official = False

    if not domain:
        return {
            "status": status, "trust_score": trust_score,
            "message": "No domain provided for verification.",
            "findings": findings, "is_official": is_official,
            "source": "internet_verification"
        }

    # --- Known official domain: skip live fetch, trust immediately ---
    if domain in ALL_OFFICIAL_DOMAINS:
        return {
            "status": "SAFE",
            "trust_score": 98,
            "message": "Domain is a verified official website.",
            "findings": ["Domain matched known official brand registry."],
            "is_official": True,
            "source": "internet_verification"
        }

    fetch_url = "https://" + domain
    positive_signals = 0
    negative_signals = 0

    try:
        resp = requests.get(
            fetch_url,
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
            allow_redirects=True,
            verify=True   # enforce SSL verification
        )

        findings.append(f"Site responded with HTTP {resp.status_code}.")

        # 1. HTTP 200 is a good sign
        if resp.status_code == 200:
            positive_signals += 2
        elif resp.status_code in (301, 302, 307, 308):
            positive_signals += 1
            findings.append("Site uses redirects (normal for legitimate sites).")
        elif resp.status_code >= 400:
            negative_signals += 2
            findings.append(f"Site returned error status {resp.status_code}.")

        # 2. SSL was valid (requests didn't throw on verify=True)
        positive_signals += 2
        findings.append("Valid SSL/TLS certificate confirmed.")

        # 3. Page title check — does it mention the domain name?
        html = resp.text[:15000].lower()
        title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else ""

        if title:
            findings.append(f"Page title: \"{title[:80]}\"")
            # Title contains domain name or brand → good signal
            domain_name = domain.split('.')[0]
            if domain_name in title.lower():
                positive_signals += 2
                findings.append("Page title matches domain name.")

        # 4. Has basic trust markers (privacy policy, contact, about)
        trust_markers = ["privacy policy", "terms of service", "terms and conditions",
                         "contact us", "about us", "©", "copyright"]
        found_markers = [m for m in trust_markers if m in html]
        if len(found_markers) >= 2:
            positive_signals += 2
            findings.append(f"Site has standard trust markers ({len(found_markers)} found).")
        elif len(found_markers) == 1:
            positive_signals += 1

        # 5. Redirect to a completely different domain is suspicious
        final_domain = urlparse(resp.url).netloc.lower().replace("www.", "")
        if final_domain and final_domain != domain:
            negative_signals += 1
            findings.append(f"Site redirected to a different domain: {final_domain}.")

        # 6. Very thin page (< 500 chars) is suspicious
        if len(resp.text.strip()) < 500:
            negative_signals += 2
            findings.append("Page has very little content (possible placeholder or scam page).")

    except requests.exceptions.SSLError:
        negative_signals += 3
        findings.append("SSL certificate is invalid or self-signed.")
    except requests.exceptions.ConnectionError:
        # DNS failed or connection refused
        negative_signals += 4
        findings.append("Domain does not resolve or refused connection (likely non-existent).")
    except requests.exceptions.Timeout:
        negative_signals += 1
        findings.append("Site took too long to respond.")
    except Exception as e:
        negative_signals += 1
        findings.append(f"Unexpected error during live check: {str(e)[:80]}")

    # --- Score based on signals ---
    net = positive_signals - negative_signals

    if net >= 4:
        status = "SAFE"
        trust_score = 85
        is_official = True
        message = "Live verification passed. Site appears legitimate."
    elif net >= 1:
        status = "LIKELY_SAFE"
        trust_score = 68
        is_official = True
        message = "Site shows signs of legitimacy but could not be fully verified."
    elif net == 0:
        status = "SUSPICIOUS"
        trust_score = 45
        message = "Verification inconclusive. Proceed with caution."
    else:
        status = "FAKE"
        trust_score = 15
        message = "Live verification failed. Site shows strong signs of being fake or malicious."

    return {
        "status": status,
        "trust_score": trust_score,
        "message": message,
        "findings": findings,
        "is_official": is_official,
        "source": "internet_verification"
    }


def analyze_url_rules(domain, normalized_url):
    """
    Rule-based structural analysis of the URL itself.
    Does NOT fetch the page — purely structural heuristics.
    """
    findings = []
    deductions = 0
    is_shortened = False

    if not domain:
        return {"risk_score": 0, "findings": findings, "is_shortened": False}

    # 1. Shortener detection
    if domain.lower() in SHORTENERS:
        is_shortened = True
        deductions += 40
        findings.append("Shortened URL detected — destination is hidden.")

    # 2. Brand impersonation / typosquat check
    brand, is_official_brand = _detect_brand_impersonation(domain)
    if brand and not is_official_brand:
        deductions += 60
        findings.append(f"Possible impersonation of '{brand}' — this is NOT the official domain.")
    elif brand and is_official_brand:
        # Official brand domain — give a trust boost signal (no deduction)
        findings.append(f"Domain is the official '{brand}' website.")

    # 3. Structural URL red flags (only on non-official domains)
    if not is_official_brand:
        from trust_pipeline.utils import ensure_scheme
        full_url = ensure_scheme(normalized_url)
        parsed = urlparse(full_url)
        path = parsed.path.lower()
        query = parsed.query.lower()

        # Deceptive path segments
        deceptive_paths = ["verify", "login", "account", "secure", "update", "billing", "payment", "confirm"]
        for pattern in deceptive_paths:
            if f"/{pattern}" in path:
                deductions += 18
                findings.append(f"Suspicious path segment: '/{pattern}'.")
            if f"{pattern}=" in query:
                deductions += 12
                findings.append(f"Sensitive query parameter: '{pattern}='.")

        # Excessive hyphens
        if domain.count("-") >= 2:
            deductions += 15
            findings.append("Domain has excessive hyphens (common impersonation tactic).")

        # Long randomised path
        if len(path) > 60 and sum(c.isdigit() for c in path) > 5:
            deductions += 10
            findings.append("Excessively long randomised path (common in phishing links).")

        # IP address as domain
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain):
            deductions += 50
            findings.append("URL uses a raw IP address instead of a domain name.")

        # Suspicious subdomains (e.g. paypal.com.evil.net)
        parts = domain.split(".")
        if len(parts) > 3:
            subdomain = ".".join(parts[:-2])
            for brand_name in KNOWN_BRANDS:
                if brand_name in subdomain:
                    deductions += 55
                    findings.append(f"Brand name '{brand_name}' found in subdomain — classic phishing pattern.")
                    break

    return {
        "risk_score": deductions,
        "findings": findings,
        "is_shortened": is_shortened
    }
