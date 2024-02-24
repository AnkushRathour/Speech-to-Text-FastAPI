from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi import Response
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.openapi.utils import get_openapi
import os
import requests

"""
    API to Transcribe audio or video from URL
    Generate Transcript in SRT, VTT, JSON and RAW format
"""

app = FastAPI()

TMP_DIR = "tmp/"

def fetch_audio_from_url(url: str) -> bytes:
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def transcribe_audio(audio_content: bytes, subtitle_format: str):
    # Save the audio content to a temporary file
    audio_file_path = os.path.join(TMP_DIR, "temp_audio.mp3")
    with open(audio_file_path, "wb") as audio_file:
        audio_file.write(audio_content)

    # Use autosub to transcribe the original audio file
    os.system(f"autosub {audio_file_path} --format {subtitle_format}")

    # Read the generated subtitle file
    subtitle_path = audio_file_path.replace(".mp3", f".{subtitle_format}")
    with open(subtitle_path, 'r') as subtitle_file:
        transcript = subtitle_file.read()

    # Clean up temporary files
    os.remove(subtitle_path)
    os.remove(audio_file_path)

    return transcript

@app.post("/transcribe")
async def transcribe(
    url: str,
    subtitle_format: str = Query("vtt", regex="^(srt|vtt|json|raw)$")
):
    audio_content = fetch_audio_from_url(url)
    if not audio_content:
        raise HTTPException(status_code=500, \
            detail="Failed to fetch audio from the provided URL.")

    transcript = transcribe_audio(audio_content, subtitle_format)

    if subtitle_format == 'json':
        return Response(transcript, media_type="application/json")
    return PlainTextResponse(transcript)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Speech To Text",
        version="v1",
        description="Generate Transcript in SRT, VTT, RAW and JSON format",
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
