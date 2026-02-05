import json
import os

def save_evidence(evidence: dict):
    os.makedirs("logs", exist_ok=True)

    with open("logs/evidence_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(evidence) + "\n")
