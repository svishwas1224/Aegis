import requests
import re
import ssl
import socket
from urllib.parse import urlparse
from difflib import SequenceMatcher
from trust_pipeline.config import REQUEST_TIMEOUT

# Optional Playwright import for JavaScript rendering
PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    pass

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


def _count_scam_keywords_in_domain(domain):
    """Count how many scam-related words appear in the domain name itself."""
    domain_lower = domain.lower().replace("-", " ").replace(".", " ")
    return [kw for kw in SCAM_DOMAIN_KEYWORDS if kw in domain_lower]


def _fetch_with_playwright(url: str):
    """Optional JavaScript rendering with Playwright"""
    if not PLAYWRIGHT_AVAILABLE:
        return None, "Playwright not available"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            page.set_default_timeout(REQUEST_TIMEOUT * 1000)  # Convert seconds to ms
            response = page.goto(url, wait_until="networkidle")
            raw_html = page.content()
            final_url = page.url
            browser.close()
            return (raw_html, final_url, response.status if response else 200), None
    except Exception as e:
        return None, str(e)


def internet_verify_official(user_input, domain=None):
    """
    Real-time live verification of a domain.
    Checks: DNS resolution, HTTPS/SSL, HTTP status, page title,
    brand match, and redirect behaviour.
    Does NOT penalise sites for having normal e-commerce words.
    Returns raw HTML for tri-engine analysis.
    """
    findings = []
    status = "UNKNOWN"
    trust_score = 50
    is_official = False
    raw_html = None

    if not domain:
        return {
            "status": status, "trust_score": trust_score,
            "message": "No domain provided for verification.",
            "findings": findings, "is_official": is_official,
            "source": "internet_verification", "raw_html": raw_html
        }

    # --- Known official domain: add to findings, but still do full live fetch! ---
    if domain in ALL_OFFICIAL_DOMAINS:
        findings.append("Domain matched known official brand registry.")
        is_official = True

    fetch_url = "https://" + domain
    positive_signals = 0
    negative_signals = 0
    html = ""
    final_url = fetch_url

    # Try Playwright first for JS rendering, fallback to requests
    playwright_success = False
    if PLAYWRIGHT_AVAILABLE:
        try:
            playwright_data, playwright_error = _fetch_with_playwright(fetch_url)
            if playwright_data and not playwright_error:
                raw_html, final_url, status_code = playwright_data
                findings.append(f"Site responded with HTTP {status_code} (JS-rendered).")
                playwright_success = True
                
                if status_code == 200:
                    positive_signals += 2
                elif 300 <= status_code < 400:
                    positive_signals += 1
                    findings.append("Site uses redirects (normal for legitimate sites).")
                elif status_code >= 400:
                    negative_signals += 2
                    findings.append(f"Site returned error status {status_code}.")
                
                positive_signals += 2  # SSL valid if Playwright got this far
                findings.append("Valid SSL/TLS certificate confirmed.")
        except Exception as e:
            findings.append(f"JS rendering failed, falling back to basic scraping: {str(e)[:50]}")
    
    # Fallback to requests if Playwright not available or failed
    if not playwright_success:
        try:
            resp = requests.get(
                fetch_url,
                timeout=REQUEST_TIMEOUT,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                allow_redirects=True,
                verify=True   # enforce SSL verification
            )

            raw_html = resp.text
            findings.append(f"Site responded with HTTP {resp.status_code} (basic scraping).")

            if resp.status_code == 200:
                positive_signals += 2
            elif resp.status_code in (301, 302, 307, 308):
                positive_signals += 1
                findings.append("Site uses redirects (normal for legitimate sites).")
            elif resp.status_code >= 400:
                negative_signals += 2
                findings.append(f"Site returned error status {resp.status_code}.")

            positive_signals += 2
            findings.append("Valid SSL/TLS certificate confirmed.")
            final_url = resp.url
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
    
    # Process the HTML we got (from either Playwright or requests)
    if raw_html:
        html = raw_html[:15000].lower()
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

        final_domain = urlparse(final_url).netloc.lower().replace("www.", "")
        if final_domain and final_domain != domain:
            negative_signals += 1
            findings.append(f"Site redirected to a different domain: {final_domain}.")

        if len(raw_html.strip()) < 500:
            negative_signals += 2
            findings.append("Page has very little content (possible placeholder or scam page).")

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
        "findings": findings, "is_official": is_official, "source": "internet_verification",
        "raw_html": raw_html
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

        # Scam keywords in domain
        domain_scam_words = _count_scam_keywords_in_domain(domain)
        if len(domain_scam_words) >= 2:
            deductions += 50
            findings.append(f"Domain name contains multiple scam-related words: {', '.join(domain_scam_words)}.")
        elif len(domain_scam_words) == 1:
            deductions += 25
            findings.append(f"Domain name contains a suspicious keyword: '{domain_scam_words[0]}'.")

        # Suspicious TLD combinations with scam keywords
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
