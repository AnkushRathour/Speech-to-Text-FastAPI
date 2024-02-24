from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi import Response
from fastapi.responses import PlainTextResponse
from fastapi.openapi.utils import get_openapi
import os

"""
    API to Transcribe local audio or video file
    Generate Transcript in SRT, VTT, JSON and RAW format
"""

app = FastAPI()
TMP_DIR = "tmp/"

def transcribe_audio(file_path, subtitle_format: str):
    # transcribe file using autosub and ffmpeg
    os.system(f"autosub {file_path} --format {subtitle_format}")

    subtitle_path = file_path.replace(".mp3", f".{subtitle_format}")
    with open(subtitle_path, 'r') as subtitle_file:
        transcript = subtitle_file.read()

    # remove file from tmp
    os.remove(subtitle_path)
    os.remove(file_path)

    return transcript

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    subtitle_format: str = Query("vtt", regex="^(srt|vtt|json|raw)$")
):
    file_formats = [
        "audio/mpeg", "audio/mp3", "audio/mp4", "audio/wav",
        "video/mpeg", "video/mp3", "video/mp4", "video/wav"
    ]
    if file.content_type not in file_formats:
        raise HTTPException(status_code=415, detail="Unsupported File Type. Please upload an Media file.")

    file_path = os.path.join(TMP_DIR, file.filename)

    # Create the /tmp/ directory if it doesn't exist
    os.makedirs(TMP_DIR, exist_ok=True)

    # Ensure file is written correctly
    with open(file_path, "wb") as audio_file:
        audio_file.write(file.file.read())

    # Verify that the file is created and has content
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        raise HTTPException(status_code=500, detail="Failed to save the audio file.")

    transcript = transcribe_audio(file_path, subtitle_format)

    if subtitle_format == 'json':
        return Response(transcript, media_type="application/json")
    return PlainTextResponse(transcript)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Speech To Text API",
        version="v1",
        description="Generate Transcript in SRT, VTT, RAW and JSON format",
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
