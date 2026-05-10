from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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
# FRONTEND PAGE
# -----------------------------

@app.get("/", response_class=HTMLResponse)
def frontend():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SHL Chatbot</title>

        <style>
            body{
                font-family: Arial;
                background:#f4f4f4;
                padding:40px;
            }

            .container{
                background:white;
                padding:30px;
                border-radius:10px;
                max-width:700px;
                margin:auto;
            }

            input{
                width:100%;
                padding:12px;
                margin-top:10px;
            }

            button{
                margin-top:10px;
                padding:12px 20px;
                background:#4CAF50;
                color:white;
                border:none;
                cursor:pointer;
            }

            .response{
                margin-top:20px;
                padding:15px;
                background:#eeeeee;
                border-radius:8px;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>🤖 SHL Assessment Recommendation Bot</h1>

            <input
                type="text"
                id="userInput"
                placeholder="Enter hiring requirements"
            >

            <button onclick="sendMessage()">
                Send
            </button>

            <div class="response" id="response"></div>

        </div>

        <script>

            async function sendMessage(){

                const input =
                    document.getElementById("userInput").value;

                const response =
                    await fetch("/chat", {

                    method:"POST",

                    headers:{
                        "Content-Type":"application/json"
                    },

                    body: JSON.stringify({
                        messages:[
                            {
                                role:"user",
                                content:input
                            }
                        ]
                    })
                });

                const data = await response.json();

                let html =
                    "<h3>" + data.reply + "</h3>";

                if(data.recommendations){

                    html += "<ul>";

                    data.recommendations.forEach(rec => {

                        html += `
                            <li>
                                <b>${rec.name}</b>
                                (${rec.test_type})
                                <br>
                                <a href="${rec.url}" target="_blank">
                                    View Assessment
                                </a>
                            </li>
                            <br>
                        `;
                    });

                    html += "</ul>";
                }

                document.getElementById("response").innerHTML = html;
            }

        </script>

    </body>
    </html>
    """

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

    # Compare
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
        "reply": "Here are recommended SHL assessments.",
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
        port=int(os.environ.get("PORT", 8000))
    )