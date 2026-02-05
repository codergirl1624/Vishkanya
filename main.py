import os
import re
import requests
from typing import List, Optional
from fastapi import FastAPI, Header, HTTPException, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ----------------
X_API_KEY = os.getenv("X_API_KEY", "VISH_KANYA_KEY")
GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

app = FastAPI(title="GUVI Agentic HoneyPot API")

# ---------------- MODELS ----------------
class Message(BaseModel):
    sender: str
    text: str
    timestamp: str

class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = []
    metadata: Optional[dict] = None

# ---------------- SCAM DETECTION ----------------
def detect_scam(text: str) -> bool:
    scam_words = ["blocked", "kyc", "verify", "urgent", "upi", "otp", "suspend"]
    return any(word in text.lower() for word in scam_words)

# ---------------- INTEL EXTRACTION ----------------
def extract_intelligence(text: str):
    return {
        "upiIds": re.findall(r"[a-zA-Z0-9.\-_]+@[a-zA-Z]+", text),
        "bankAccounts": re.findall(r"\b\d{9,18}\b", text),
        "phishingLinks": re.findall(r"https?://[^\s]+", text),
        "phoneNumbers": re.findall(r"\+?\d{10,12}", text),
        "suspiciousKeywords": [w for w in ["blocked", "urgent", "verify", "kyc"] if w in text.lower()]
    }

# ---------------- AGENT REPLY ----------------
def agent_reply(text: str) -> str:
    # Multi-hook trick (simple rule based)
    if "@" in text:
        return "I tried sending but it says payment failed… do you have another UPI ID?"

    return "Oh no… my account is very important. What should I do now?"

# ---------------- GUVI CALLBACK ----------------
def send_callback(session_id, history, message_text):
    intel = extract_intelligence(message_text)

    payload = {
        "sessionId": session_id,
        "scamDetected": True,
        "totalMessagesExchanged": len(history) + 1,
        "extractedIntelligence": intel,
        "agentNotes": "Agent engaged scammer using delay + payment failure hook."
    }

    try:
        res = requests.post(GUVI_CALLBACK_URL, json=payload, timeout=5)
        print("✅ GUVI CALLBACK SENT:", res.status_code)
    except Exception as e:
        print("❌ CALLBACK FAILED:", e)

# ---------------- API ENDPOINT ----------------
@app.post("/analyze")
async def analyze(
    data: ScamRequest,
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(...)
):
    # API KEY SECURITY
    if x_api_key != X_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Detect scam
    scam = detect_scam(data.message.text)

    if scam:
        # Background callback
        background_tasks.add_task(
            send_callback,
            data.sessionId,
            data.conversationHistory,
            data.message.text
        )

        reply = agent_reply(data.message.text)

        return {
            "status": "success",
            "reply": reply
        }

    return {
        "status": "success",
        "reply": "Hello, can you explain more?"
    }

# ---------------- HEALTH CHECK ----------------
@app.get("/")
def home():
    return {"status": "🟢 HoneyPot Engine Online"}
