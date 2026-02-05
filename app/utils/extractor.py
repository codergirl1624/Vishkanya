import re

def extract_entities(text: str):
    upi_pattern = r"\b[\w.\-]+@[\w]+\b"
    url_pattern = r"https?://\S+"

    return {
        "upi_ids": re.findall(upi_pattern, text),
        "urls": re.findall(url_pattern, text)
    }
