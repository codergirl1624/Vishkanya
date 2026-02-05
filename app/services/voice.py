import hashlib

def voice_fingerprint(fake_audio_text: str):
    return hashlib.sha256(fake_audio_text.encode()).hexdigest()
