from dotenv import load_dotenv
import logging
import pvporcupine
import pyaudio
import struct
import os
from .record_audio import record_audio
from .transcription import transcribe_and_save
from .chat_interface import main as chat_interface_main
import keyboard
import time

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
ACCESS_KEY = os.getenv("PORCUPINE_ACCESS_KEY")
KEYWORD_PATH = os.getenv("PORCUPINE_KEYWORD_PATH")
TRANSCRIPTION_OUTPUT = os.getenv("TRANSCRIPTION_OUTPUT")

logger.debug(f"ACCESS_KEY: {'Set' if ACCESS_KEY else 'Not set'}")
logger.debug(f"KEYWORD_PATH: {KEYWORD_PATH}")
logger.debug(f"TRANSCRIPTION_OUTPUT: {TRANSCRIPTION_OUTPUT}")

if not ACCESS_KEY or not KEYWORD_PATH:
    raise ValueError("Environment variables for Porcupine are not set properly.")

def listen_for_wakeword():
    porcupine = None
    pa = None
    audio_stream = None

    try:
        logger.info("Initializing Porcupine...")
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[KEYWORD_PATH]
        )
        logger.info("Porcupine initialized successfully.")

        logger.info("Initializing PyAudio...")
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        logger.info("PyAudio initialized successfully.")

        logger.info("Listening for 'Hey Amy'...")

        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                logger.info("Wake word detected!")
                recorded_file = record_audio()
                transcription_file = transcribe_and_save(recorded_file)
                chat_interface_main(transcription_file)
                
                logger.info("Press 'r' to record the next message or 'q' to quit.")
                while True:
                    if keyboard.is_pressed('r'):
                        logger.info("Recording next message...")
                        break
                    elif keyboard.is_pressed('q'):
                        logger.info("Quitting...")
                        return
                    time.sleep(0.1)

    except pvporcupine.PorcupineInvalidArgumentError as e:
        logger.error(f"Porcupine initialization error: {str(e)}")
    except pyaudio.PyAudioError as e:
        logger.error(f"PyAudio initialization error: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
    finally:
        logger.info("Cleaning up resources...")
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
        logger.info("Cleanup complete.")

if __name__ == "__main__":
    listen_for_wakeword()