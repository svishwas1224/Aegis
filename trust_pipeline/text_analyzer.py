import re
import os
import pickle
from trust_pipeline.config import TRUST_SCORE_TEXT_LOW_RISK, TRUST_SCORE_TEXT_POTENTIALLY_SUSPICIOUS, TRUST_SCORE_TEXT_SUSPICIOUS

# ── Load ML model once at import time ───────────────────────────────────────
_MODEL = None
_MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "dark_pattern_model.pkl")

def _load_model():
    global _MODEL
    if _MODEL is None:
        try:
            with open(_MODEL_PATH, "rb") as f:
                _MODEL = pickle.load(f)
            print("[INFO] Dark pattern ML model loaded successfully.")
        except Exception as e:
            print(f"[WARN] Could not load ML model: {e}")
            _MODEL = None
    return _MODEL

_load_model()

# Category descriptions shown to the user
CATEGORY_DESCRIPTIONS = {
    "Urgency":              "Creates artificial time pressure to force a quick decision.",
    "Scarcity":             "Falsely implies limited availability to pressure purchase.",
    "Sneaking":             "Hides costs, subscriptions, or items added without consent.",
    "Misdirection":         "Draws attention away from important information.",
    "Social Proof":         "Uses fake or manipulated reviews/counts to influence behaviour.",
    "Forced Action":        "Forces users to perform unwanted actions to proceed.",
    "Obstruction":          "Makes it deliberately hard to cancel, unsubscribe, or opt out.",
    "General Dark Pattern": "Contains manipulative design or language patterns.",
    "Not Dark Pattern":     None,  # safe — no description needed
}

# Regex patterns for scam/phishing text (separate from e-commerce dark patterns)
SCAM_PATTERNS = [
    (r"\burgent\b",                                                    12, "Urgency"),
    (r"\bimmediately\b",                                               10, "Urgency"),
    (r"\bfinal warning\b",                                             20, "Urgency"),
    (r"\bwithin \d+ (hour|minute|day)",                                15, "Urgency"),
    (r"\b(24|48) hours?\b",                                            12, "Urgency"),
    (r"\bbefore (it )?expires?\b",                                     15, "Urgency"),
    (r"\bexpires? (today|tonight|at midnight)",                        15, "Urgency"),
    (r"\bact now\b",                                                   12, "Urgency"),
    (r"\bwill be (blocked|suspended|deactivated|removed|deleted|terminated)", 20, "Urgency"),
    (r"\bpermanent(ly)? (suspend|block|deactivat|delet)",              20, "Urgency"),
    (r"\bverify (your )?(account|identity|number|details|information)", 15, "Forced Action"),
    (r"\bconfirm (your )?(account|identity|details|ownership)",        15, "Forced Action"),
    (r"\bbank account\b",                                              10, "Sneaking"),
    (r"\bsuspicious activity\b",                                       15, "Misdirection"),
    (r"\bunusual (login|activity|access)\b",                           15, "Misdirection"),
    (r"\bkyc\b",                                                       18, "Forced Action"),
    (r"\bkyc (is )?incomplete\b",                                      20, "Forced Action"),
    (r"\bupdate (your )?(payment|billing|card)\b",                     15, "Sneaking"),
    (r"\bpayment (could not|failed|was not) processed\b",              18, "Sneaking"),
    (r"\btax refund\b",                                                18, "Misdirection"),
    (r"\bgovernment (assistance|benefit|scheme)\b",                    18, "Misdirection"),
    (r"\bsmall (re-?delivery )?fee\b",                                 20, "Sneaking"),
    (r"\byou (have |'ve )?(won|been selected|been chosen)\b",          20, "Social Proof"),
    (r"\bcongratulations\b",                                           10, "Social Proof"),
    (r"\bcashback (reward|bonus)\b",                                   15, "Scarcity"),
    (r"\bexclusive (reward|offer|cashback)\b",                         12, "Scarcity"),
    (r"\bredeem before\b",                                             15, "Urgency"),
    (r"\blimited.time offer\b",                                        12, "Urgency"),
    (r"\bpackage (is )?on hold\b",                                     18, "Forced Action"),
    (r"\bshipment (is )?delayed\b",                                    12, "Misdirection"),
    (r"\bsim (card )?(will be |is )?blocked\b",                        20, "Urgency"),
    (r"\baccount (will be |may be )?removed\b",                        18, "Urgency"),
    (r"\bunless you confirm\b",                                        15, "Forced Action"),
    (r"\bonly \d+ left\b",                                             15, "Scarcity"),
    (r"\bhurry\b",                                                     12, "Urgency"),
    (r"\bflash sale\b",                                                10, "Urgency"),
    (r"\bin demand\b",                                                 10, "Scarcity"),
    (r"\bno thanks i (prefer|don.t want)\b",                           20, "Misdirection"),
    (r"\bmust (register|sign up) to proceed\b",                        15, "Forced Action"),
    (r"\bmandatory signup\b",                                          15, "Forced Action"),
]


def _ml_classify(text):
    """
    Run the ML model on a piece of text.
    Returns list of (category, confidence) tuples for non-safe predictions.
    """
    model = _MODEL
    if model is None:
        return []

    try:
        proba = model.predict_proba([text])[0]
        classes = model.classes_
        results = []
        for cls, prob in zip(classes, proba):
            if cls != "Not Dark Pattern" and prob >= 0.20:
                results.append((cls, round(float(prob) * 100, 1)))
        # Sort by confidence descending
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    except Exception as e:
        print(f"[WARN] ML inference failed: {e}")
        return []


def analyze_text_input(text):
    cleaned = text.strip()
    lower_text = cleaned.lower()

    # ── 1. Regex-based scam pattern detection ───────────────────────────────
    regex_score = 0
    category_hits = {}  # category -> score accumulation

    for pattern, weight, category in SCAM_PATTERNS:
        if re.search(pattern, lower_text):
            regex_score += weight
            category_hits[category] = category_hits.get(category, 0) + weight

    # ── 2. ML model classification ───────────────────────────────────────────
    ml_results = _ml_classify(cleaned)

    # Merge ML categories into category_hits
    for category, confidence in ml_results:
        # Convert confidence % to a score contribution
        ml_weight = int(confidence * 0.4)  # 100% confidence = 40 pts
        category_hits[category] = category_hits.get(category, 0) + ml_weight
        regex_score += ml_weight

    # ── 3. Build findings list ───────────────────────────────────────────────
    findings = []

    # Add ML-detected categories with confidence
    for category, confidence in ml_results:
        desc = CATEGORY_DESCRIPTIONS.get(category, "Manipulative pattern detected.")
        findings.append(f"{category} ({confidence}% confidence) — {desc}")

    # Add regex-detected categories not already covered by ML
    ml_categories = {c for c, _ in ml_results}
    for category, score in sorted(category_hits.items(), key=lambda x: x[1], reverse=True):
        if category not in ml_categories and category in CATEGORY_DESCRIPTIONS:
            desc = CATEGORY_DESCRIPTIONS.get(category, "")
            if desc:
                findings.append(f"{category} — {desc}")

    # Remove duplicates
    seen = set()
    unique_findings = []
    for f in findings:
        if f not in seen:
            seen.add(f)
            unique_findings.append(f)

    # ── 4. Final verdict ─────────────────────────────────────────────────────
    if regex_score >= 40:
        status = "SUSPICIOUS"
        trust_score = TRUST_SCORE_TEXT_SUSPICIOUS
        message = "High-risk manipulation patterns detected in this content."
    elif regex_score >= 15:
        status = "SUSPICIOUS"
        trust_score = TRUST_SCORE_TEXT_POTENTIALLY_SUSPICIOUS
        message = "This content contains patterns commonly used in scams or dark UX."
    else:
        status = "SAFE"
        trust_score = TRUST_SCORE_TEXT_LOW_RISK
        message = "No suspicious patterns detected."

    return {
        "status": status,
        "trust_score": trust_score,
        "message": message,
        "patterns_found": len(unique_findings),
        "findings": unique_findings,
        "ml_categories": [{"category": c, "confidence": conf} for c, conf in ml_results],
    }
