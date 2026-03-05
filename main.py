from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from fastapi import HTTPException
import json

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
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                 {
                    "role": "system",
                    "content": """
                    You are a senior analyst.
                    Return ONLY valid JSON in this format:
                    {
                      "summary": "string",
                      "sentiment": "positive | neutral | negative",
                      "key_points": ["point1", "point2"]
                    }
                    Do not include any extra text.
                    """
                },
                {"role": "user", "content": request.text}
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content

        parsed = json.loads(content)

        return parsed
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Model returned invalid JSON")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))