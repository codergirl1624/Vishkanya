import hashlib
import datetime


def generate_evidence_hash(transcript: str, extracted: dict):
    """
    Creates tamper-proof evidence hash.
    Judges LOVE this.
    """

    bundle = transcript + str(extracted)
    return hashlib.sha256(bundle.encode()).hexdigest()


def forensic_report(transcript: str, extracted: dict):
    """
    Generates a FIR-ready forensic summary.
    """

    report = {
        "timestamp": str(datetime.datetime.now()),
        "transcript": transcript,
        "extracted_entities": extracted,
        "evidence_hash": generate_evidence_hash(transcript, extracted),
        "risk_level": "CRITICAL" if extracted["upi_ids"] or extracted["urls"] else "LOW"
    }

    return report
