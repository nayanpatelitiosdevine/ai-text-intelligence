from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO) # Set the minimum level to log


load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TextRequest(BaseModel):
    text: str

@app.get("/")
def health():
    return {"status": "AI service running"}

@app.post("/analyze")
def analyze_text(request: TextRequest):
    logging.info("Before calling OpenAI client")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a senior analyst. Return ONLY valid JSON with summary, sentiment, and key_points."},
            {"role": "user", "content": request.text}
        ],
        temperature=0.3
    )
    logging.info("After calling OpenAI client")
    return {"result": response.choices[0].message.content}