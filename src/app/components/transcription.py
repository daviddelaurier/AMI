import os
import time
import logging
from dotenv import load_dotenv
import pyaudio
import wave
import numpy as np
from colorama import init, Fore, Style
from datetime import datetime
import threading
from groq import Groq
from .record_audio import record_audio

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
TRANSCRIPTION_OUTPUT = os.getenv("TRANSCRIPTION_OUTPUT", "transcription.txt")

# Ensure output directory exists and create a folder for today
def get_daily_output_path():
    today = datetime.now().strftime("%Y-%m-%d")
    daily_path = os.path.join(TRANSCRIPTION_OUTPUT, today)
    os.makedirs(daily_path, exist_ok=True)
    return daily_path

def transcribe_audio(audio_file, model="whisper-large-v3", prompt=None, response_format="text", language=None, temperature=0.0):
    logger.info(f"Transcribing audio file: {audio_file}")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    client = Groq(api_key=api_key)
    with open(audio_file, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,
            model=model,
            prompt=prompt,
            response_format=response_format,
            language=language,
            temperature=temperature
        )
    return transcription

def save_transcription(result, audio_file):
    if result is None:
        logger.error("Transcription failed. No result to save.")
        return None

    daily_path = get_daily_output_path()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    transcription_file = os.path.join(daily_path, f"transcription_{timestamp}.txt")
    with open(transcription_file, 'w', encoding='utf-8') as f:
        if hasattr(result, 'text'):
            f.write(result.text)
        else:
            f.write(str(result))
    logger.info(f"Transcription saved to {transcription_file}")
    return transcription_file

def transcribe_and_save(audio_file):
    result = transcribe_audio(audio_file)
    transcription_file = save_transcription(result, audio_file)
    return transcription_file

def transcribe_in_background(audio_file):
    threading.Thread(target=transcribe_and_save, args=(audio_file,), daemon=True).start()