from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
import time
from fastapi import HTTPException
import json

logging.basicConfig(level=logging.INFO) # Set the minimum level to log
logger = logging.getLogger(__name__)

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
    start_time = time.time()
    logger.info("Received request to analyze text")
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
        logger.info(f"Model response received in {time.time() - start_time:.2f} seconds")
        content = response.choices[0].message.content

        parsed = json.loads(content)
        usage = response.usage
        logger.info(f"Prompt tokens: {usage.prompt_tokens}")
        logger.info(f"Completion tokens: {usage.completion_tokens}")
        logger.info(f"Total tokens: {usage.total_tokens}")
        
        return parsed
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Model returned invalid JSON")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))