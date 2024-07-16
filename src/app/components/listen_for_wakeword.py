from dotenv import load_dotenv
import logging
import pvporcupine
import pyaudio
import struct
from .record_audio import record_audio
from .transcription import transcribe_and_save
from .chat_interface import main as chat_interface_main

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os

# Load environment variables
ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")
KEYWORD_PATH = os.getenv("PORCUPINE_KEYWORD_PATH", "porcupine.txt")
TRANSCRIPTION_OUTPUT = os.getenv("TRANSCRIPTION_OUTPUT", "transcription.txt")

if not ACCESS_KEY or not KEYWORD_PATH:
    raise ValueError("Environment variables for Porcupine are not set properly.")


def listen_for_wakeword():
    porcupine = None
    pa = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[KEYWORD_PATH]
        )

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        logger.info("Listening for 'Hey Amy'...")

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                logger.info("Wake word detected!")
                recorded_file = record_audio()
                transcription_file = transcribe_and_save(recorded_file, TRANSCRIPTION_OUTPUT)
                chat_interface_main(transcription_file)
                logger.info("Listening for 'Hey Amy'...")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()

if __name__ == "__main__":
    listen_for_wakeword()