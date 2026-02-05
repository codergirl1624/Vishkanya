def guardian_check(text: str):

    jailbreak_keywords = ["ignore instructions", "system prompt", "password"]

    for word in jailbreak_keywords:
        if word in text.lower():
            return True

    return False
