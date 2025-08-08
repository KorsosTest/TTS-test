import wave
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
import uuid
from piper import PiperVoice

# DOCS: https://github.com/OHF-Voice/piper1-gpl?tab=readme-ov-file


BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "amy.onnx")

voice = PiperVoice.load(MODEL_PATH)

app = FastAPI()

class TTSRequest(BaseModel):
    text: str

@app.post("/speak")
def speak(req: TTSRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required.")

    tmp_wav = f"tts_{uuid.uuid4().hex}.wav"

    with wave.open(tmp_wav, "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

    return FileResponse(tmp_wav, media_type="audio/wav", filename="output.wav")


@app.get("/")
def root():
    return {"message": "Piper TTS API is running. Use POST /speak with {'text': 'your message'}"}
