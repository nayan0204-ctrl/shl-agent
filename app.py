from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
import os

app = FastAPI()

# -----------------------------
# DATA MODELS
# -----------------------------

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# -----------------------------
# SHL ASSESSMENTS
# -----------------------------

assessments = [
    {
        "name": "Python Assessment",
        "url": "https://www.shl.com/",
        "test_type": "Technical"
    },
    {
        "name": "DevOps Assessment",
        "url": "https://www.shl.com/",
        "test_type": "Technical"
    },
    {
        "name": "Cloud Computing Assessment",
        "url": "https://www.shl.com/",
        "test_type": "Technical"
    },
    {
        "name": "Java Assessment",
        "url": "https://www.shl.com/",
        "test_type": "Technical"
    },
    {
        "name": "OPQ32r",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/opq32r/",
        "test_type": "Personality"
    },
    {
        "name": "General Ability Screen",
        "url": "https://www.shl.com/solutions/products/product-catalog/view/general-ability-screen/",
        "test_type": "Cognitive"
    }
]

# -----------------------------
# HOME
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "SHL Agent API running successfully"
    }

# -----------------------------
# HEALTH
# -----------------------------

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

# -----------------------------
# CHAT ENDPOINT
# -----------------------------

@app.post("/chat")
def chat(req: ChatRequest):

    latest_message = req.messages[-1].content.lower()

    # Greeting
    if "hello" in latest_message or "hi" in latest_message:
        return {
            "reply": "Hello! Tell me the role and skills you are hiring for.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Comparison
    if "compare" in latest_message:
        return {
            "reply": "OPQ32r measures personality traits while General Ability Screen evaluates cognitive ability.",
            "recommendations": [],
            "end_of_conversation": True
        }

    # Prompt injection protection
    if "ignore previous instructions" in latest_message:
        return {
            "reply": "I can only assist with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Recommendation logic
    matched = []

    for assessment in assessments:

        text = (
            assessment["name"] + " " +
            assessment["test_type"]
        ).lower()

        score = 0

        for word in latest_message.split():
            if word in text:
                score += 1

        if score > 0:
            matched.append((score, assessment))

    matched.sort(reverse=True, key=lambda x: x[0])

    recommendations = [x[1] for x in matched[:5]]

    if not recommendations:
        recommendations = assessments[:5]

    return {
        "reply": "Here are recommended SHL assessments for your hiring needs.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }

# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )