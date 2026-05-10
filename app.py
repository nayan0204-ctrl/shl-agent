from fastapi import FastAPI

from models.schemas import ChatRequest
from services.chat_service import chat

app = FastAPI()

@app.get("/health")
def health():

    return {
        "status": "ok"
    }

@app.post("/chat")
def chat_endpoint(request: ChatRequest):

    response = chat(
        [m.model_dump() for m in request.messages]
    )

    return response