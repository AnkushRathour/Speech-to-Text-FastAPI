# Speech To Text FastAPI

Speech To Text API using [Autosub](https://github.com/agermanidis/autosub), [FastAPI](https://fastapi.tiangolo.com/) and [Ffmpeg](https://ffmpeg.org/).

# Installation
- pip install fastapi
- pip install uvicorn
- pip install autosub
- Install Ffmpeg on your Operation System (Window, Mac, Ubunut) Check Docs for Installation process.

# How to use
[app.py](https://github.com/AnkushRathour/Speech-to-Text-FastAPI/blob/main/app.py) - Generate Transcript from url with media file
Command to start FastAPI server
- uvicorn app:app --host 0.0.0.0 --port 80 --relaod

[main.py](https://github.com/AnkushRathour/Speech-to-Text-FastAPI/blob/main/app.py) - Upload your local audio or video file and generates it transcription.
Command to start
- uvicorn main:app --host 0.0.0.0 --port 80 --relaod
