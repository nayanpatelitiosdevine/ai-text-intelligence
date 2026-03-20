# AI Text Intelligence

A simple FastAPI service for analyzing text using OpenAI's GPT models.

## Features

- Health check endpoint
- Text analysis endpoint that provides:
  - Summary of the text
  - Sentiment analysis (positive, neutral, negative)
  - Key points extraction

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Activate the virtual environment:
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running the Application

Start the server with:
```bash
uvicorn main:app --host 0.0.0.0 --port 10000
```

For development with auto-reload:
```bash
uvicorn main:app --host 0.0.0.0 --port 10000 --reload
```

Or use the Procfile for deployment on platforms like Heroku.

## API Endpoints

- `GET /` - Health check
- `POST /analyze` - Analyze text

  Request body:
  ```json
  {
    "text": "Your text to analyze here"
  }
  ```

  Response:
  ```json
  {
    "summary": "Brief summary of the text",
    "sentiment": "positive | neutral | negative",
    "key_points": ["point1", "point2", ...]
  }
  ```

## Technologies Used

- FastAPI
- OpenAI API
- Pydantic
- Python-dotenv