from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import requests
from datetime import datetime
from uuid import uuid4
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AskGPT Book Generator API",
    description="Backend service for Modern Book Generator",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    logger.error("OPENAI_API_KEY environment variable not set!")
    raise ValueError("OPENAI_API_KEY environment variable is required")

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/")
async def root():
    """Root endpoint - returns service information"""
    return {
        "service": "AskGPT Book Generator API",
        "version": "1.0.0",
        "endpoints": {
            "ask.php": "Generate text content",
            "topic.php": "Generate chapter content", 
            "image_1.php": "Generate book cover images"
        },
        "status": "running"
    }

@app.get("/ask.php")
async def ask(ask: str):
    """
    Generate text content using OpenAI GPT
    Used for generating preface and afterword content
    """
    try:
        logger.info(f"Generating text for prompt: {ask[:100]}...")
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "Du bist ein professioneller Buchautor. Schreibe hochwertige, informative und ansprechende Texte."
                },
                {"role": "user", "content": ask}
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        
        text = response.choices[0].message.content.strip()
        logger.info(f"Generated {len(text)} characters of text")
        
        return PlainTextResponse(text)
        
    except Exception as e:
        logger.error(f"Error generating text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")

@app.get("/topic.php")
async def topic(ask: str):
    """
    Generate chapter content using OpenAI GPT
    Used for generating main chapter content
    """
    try:
        logger.info(f"Generating chapter for topic: {ask[:100]}...")
        
        prompt = f"""Schreibe ein ausführliches, informatives Kapitel zum Thema: {ask}

Das Kapitel sollte enthalten:
- Eine klare Einführung zum Thema
- Detaillierte Erklärungen und Beispiele
- Praktische Anwendungen oder Fallstudien
- Eine Zusammenfassung der wichtigsten Punkte

Schreibe in einem professionellen, aber verständlichen Stil. Verwende Überschriften, Aufzählungspunkte und strukturierte Absätze für bessere Lesbarkeit."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Du bist ein erfahrener Fachautor. Schreibe strukturierte, informative Kapitel mit klarer Gliederung."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048,
            temperature=0.7,
        )
        
        text = response.choices[0].message.content.strip()
        logger.info(f"Generated {len(text)} characters for chapter")
        
        return PlainTextResponse(text)
        
    except Exception as e:
        logger.error(f"Error generating chapter: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating chapter: {str(e)}")

@app.get("/image_1.php")
async def image_1(ask: str):
    """
    Generate book cover image using DALL-E
    Used for generating book cover images
    """
    try:
        logger.info(f"Generating image for topic: {ask[:100]}...")
        
        # Create a descriptive prompt for book cover generation
        dalle_prompt = f"""Ein modernes, professionelles Buchcover zum Thema: {ask}

Das Cover sollte enthalten:
- Moderne, saubere Gestaltung
- Passende Farben und Typografie
- Professionelles Layout
- Kein Text auf dem Bild (nur visuelle Elemente)
- Hochwertige, ansprechende Darstellung

Stil: Modern, minimalistisch, professionell"""

        response = openai.Image.create(
            prompt=dalle_prompt,
            n=1,
            size="512x512"
        )
        
        image_url = response['data'][0]['url']
        
        # Download the image
        img_response = requests.get(image_url, timeout=30)
        img_response.raise_for_status()
        img_data = img_response.content
        
        # Save the image with unique filename
        filename = f"{UPLOAD_DIR}/cover_{uuid4()}.png"
        with open(filename, "wb") as f:
            f.write(img_data)
        
        logger.info(f"Generated and saved image: {filename}")
        
        return FileResponse(
            filename, 
            media_type="image/png",
            headers={"Cache-Control": "public, max-age=3600"}
        )
        
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "openai_key_configured": bool(openai.api_key)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 