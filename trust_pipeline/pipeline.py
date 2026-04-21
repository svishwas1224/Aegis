import re
from trust_pipeline.utils import detect_input_type, extract_domain_from_anything, normalize_full_url
from trust_pipeline.datasets import lookup_verified_domain, lookup_fake_domain
from trust_pipeline.verification import internet_verify_official, analyze_url_rules
from trust_pipeline.text_analyzer import analyze_text_input


def analyze_input(user_input):
    original_input = user_input.strip() if user_input else ""
    input_type = detect_input_type(original_input)

    if input_type == "invalid":
        return {
            "status": "INVALID_INPUT",
            "trust_score": 0,
            "message": "Please enter a valid URL, domain, or meaningful text.",
            "findings": []
        }

    if input_type in ("url", "domain"):
        return process_url_domain(original_input, input_type)
    return process_text(original_input)


def process_url_domain(original_input, input_type):
    domain = extract_domain_from_anything(original_input)
    findings = []

    # ── Step 1: Structural rule analysis ────────────────────────────────────
    rule_results = analyze_url_rules(domain, original_input)
    findings.extend(rule_results["findings"])
    structural_risk = rule_results["risk_score"]

    # High structural risk — return immediately, no need to fetch
    if structural_risk >= 50:
        final_score = max(0, 30 - max(0, structural_risk - 50))
        return _build_result(final_score, findings, rule_results, original_input)

    # ── Step 2: Dataset lookup ───────────────────────────────────────────────
    is_verified = lookup_verified_domain(domain) if domain else False
    is_fake = lookup_fake_domain(domain) if domain else False

    if is_fake:
        findings.append("Domain found in global malicious blacklist.")
        return _build_result(8, findings, rule_results, original_input)

    # ── Step 3: Live verification ────────────────────────────────────────────
    verify_data = internet_verify_official(original_input, domain=domain)
    live_findings = [f for f in verify_data["findings"] if f not in findings]
    findings.extend(live_findings)

    live_status = verify_data["status"]
    live_score = verify_data["trust_score"]

    # ── Step 4: Combine signals ──────────────────────────────────────────────
    # Structural risk always reduces the live score — more risk = bigger penalty
    penalty = min(structural_risk, 40)

    if live_status == "SAFE":
        final_score = max(live_score - penalty, 55)
    elif live_status == "LIKELY_SAFE":
        base = 80 if is_verified else live_score
        final_score = max(base - penalty, 45)
    elif live_status == "FAKE":
        final_score = min(live_score, 15)
    elif live_status == "SUSPICIOUS":
        base = 60 if is_verified else live_score
        final_score = max(base - penalty, 10)
    else:  # UNKNOWN
        base = 70 if is_verified else 45
        final_score = max(base - penalty, 10)

    final_score = max(0, min(100, final_score))
    return _build_result(final_score, findings, rule_results, original_input)


def _build_result(final_score, findings, rule_results, original_input):
    final_score = max(0, min(100, int(final_score)))

    if final_score >= 75:
        status = "SAFE"
        message = "Live verification passed. This site appears legitimate and trustworthy."
    elif final_score >= 45:
        status = "SUSPICIOUS"
        message = "Verification inconclusive. Some elements could not be confirmed — proceed with caution."
    else:
        status = "UNSAFE"
        message = "High-risk indicators detected. This URL shows strong signs of being fake or malicious."

    # Hard overrides
    if rule_results.get("is_shortened") or any("impersonation" in f.lower() for f in findings):
        if status == "SAFE":
            status = "SUSPICIOUS"
            final_score = min(final_score, 72)

    return {
        "status": status,
        "trust_score": final_score,
        "message": message,
        "risk_level": "HIGH" if status == "UNSAFE" else "MEDIUM" if status == "SUSPICIOUS" else "LOW",
        "patterns": findings,
        "findings": findings,
        "patterns_found": len(findings),
        "type": "url",
        "url": original_input
    }


def process_text(original_input):
    """
    Handles pure text input. Also extracts any embedded URLs and
    runs URL analysis on them, combining both scores.
    """
    text_result = analyze_text_input(original_input)
    findings = list(text_result.get("findings", []))
    text_score = text_result["trust_score"]

    # Extract any URLs embedded in the text and analyze them
    url_pattern = re.compile(
        r'https?://[^\s]+|(?:[a-zA-Z0-9-]+\.)+(?:com|net|org|in|io|co|xyz|top|info|biz|gov|edu)[^\s]*',
        re.IGNORECASE
    )
    embedded_urls = url_pattern.findall(original_input)

    worst_url_score = None
    for raw_url in embedded_urls:
        domain = extract_domain_from_anything(raw_url)
        if not domain:
            continue
        rule_results = analyze_url_rules(domain, raw_url)
        url_findings = [f"[URL: {raw_url[:50]}] {f}" for f in rule_results["findings"]]
        findings.extend(url_findings)

        structural_risk = rule_results["risk_score"]
        if structural_risk >= 50:
            url_score = max(0, 30 - max(0, structural_risk - 50))
        else:
            is_fake = lookup_fake_domain(domain)
            if is_fake:
                url_score = 8
                findings.append(f"[URL: {raw_url[:50]}] Domain found in malicious blacklist.")
            else:
                verify_data = internet_verify_official(raw_url, domain=domain)
                live_status = verify_data["status"]
                live_score = verify_data["trust_score"]
                penalty = min(structural_risk, 40)
                if live_status == "SAFE":
                    url_score = max(live_score - penalty, 55)
                elif live_status == "FAKE":
                    url_score = min(live_score, 15)
                else:
                    url_score = max(live_score - penalty, 10)

        if worst_url_score is None or url_score < worst_url_score:
            worst_url_score = url_score

    # Final score = worst of text score and URL score
    if worst_url_score is not None:
        final_score = min(text_score, worst_url_score)
    else:
        final_score = text_score

    final_score = max(0, min(100, int(final_score)))

    if final_score >= 75:
        status = "SAFE"
        message = "No suspicious patterns detected in the content."
    elif final_score >= 45:
        status = "SUSPICIOUS"
        message = "This message contains patterns commonly used in scams or phishing attempts."
    else:
        status = "UNSAFE"
        message = "High-risk content detected. This message shows strong signs of being a scam."

    return {
        "status": status,
        "trust_score": final_score,
        "message": message,
        "risk_level": "HIGH" if status == "UNSAFE" else "MEDIUM" if status == "SUSPICIOUS" else "LOW",
        "patterns": findings,
        "findings": findings,
        "patterns_found": len(findings),
        "type": "text",
        "url": original_input[:60] + ("..." if len(original_input) > 60 else "")
    }
