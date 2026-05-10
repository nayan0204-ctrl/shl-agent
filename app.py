from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

# Home route for Railway health check
@app.get("/")
def home():
    return {"message": "API running successfully"}

# Example API route
@app.get("/test")
def test():
    return {"status": "working"}

# Run server
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )