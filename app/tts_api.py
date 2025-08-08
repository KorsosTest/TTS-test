import wave
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
import uuid
from piper import PiperVoice

# DOCS: https://github.com/OHF-Voice/piper1-gpl?tab=readme-ov-file


base_dir = os.path.dirname(__file__)
voice_model_path = os.path.join(base_dir, "amy.onnx")

voice = PiperVoice.load(voice_model_path)

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
