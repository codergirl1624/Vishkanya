# app/utils/harvest.py

import re
from datetime import datetime


# -----------------------------
# REGEX PATTERNS (Evidence Rules)
# -----------------------------

UPI_PATTERN = r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"

BANK_ACCOUNT_PATTERN = r"\b\d{9,18}\b"

IFSC_PATTERN = r"\b[A-Z]{4}0[A-Z0-9]{6}\b"

PHONE_PATTERN = r"\b(\+91[-\s]?)?[6-9]\d{9}\b"

URL_PATTERN = r"(https?:\/\/[^\s]+)"


# -----------------------------
# MAIN HARVEST FUNCTION
# -----------------------------

def harvest_evidence(text: str) -> dict:
    """
    Extract scam-related evidence from conversation text.
    Returns structured fraud intelligence.
    """

    upi_ids = re.findall(UPI_PATTERN, text)
    bank_accounts = re.findall(BANK_ACCOUNT_PATTERN, text)
    ifsc_codes = re.findall(IFSC_PATTERN, text)
    phone_numbers = re.findall(PHONE_PATTERN, text)
    urls = re.findall(URL_PATTERN, text)

    evidence = {
        "timestamp": datetime.now().isoformat(),

        "extracted": {
            "upi_ids": list(set(upi_ids)),
            "bank_accounts": list(set(bank_accounts)),
            "ifsc_codes": list(set(ifsc_codes)),
            "phone_numbers": list(set(phone_numbers)),
            "urls": list(set(urls)),
        },

        "risk_score": calculate_risk_score(
            upi_ids, bank_accounts, urls
        )
    }

    return evidence


# -----------------------------
# RISK SCORING SYSTEM
# -----------------------------

def calculate_risk_score(upi_ids, bank_accounts, urls) -> int:
    """
    Simple fraud risk scoring.
    """

    score = 0

    if len(upi_ids) > 0:
        score += 40

    if len(bank_accounts) > 0:
        score += 40

    if len(urls) > 0:
        score += 20

    return min(score, 100)

from app.utils.extractor import extract_entities
from app.services.forensics import forensic_report


def harvest_agent(transcript: str):

    extracted = extract_entities(transcript)

    report = forensic_report(transcript, extracted)

    return report


# -----------------------------
# DEMO TEST RUN
# -----------------------------
if __name__ == "__main__":
    sample = """
    Hello sir, send money to my UPI: fraudster@paytm
    Also click this link: https://fakebank-login.com
    My account number is 123456789012
    IFSC is HDFC0001234
    """

    result = harvest_evidence(sample)

    print("\n🚨 Extracted Evidence:\n")
    print(result)
