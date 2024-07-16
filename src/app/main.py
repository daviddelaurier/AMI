import logging
import pygame
import os
import time
from dotenv import load_dotenv
from components.record_audio import record_audio
from components.transcription import transcribe_and_save
from components.listen_for_wakeword import listen_for_wakeword
from components.chat_interface import main as chat_interface_main, play_audio

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize pygame mixer once
pygame.mixer.init()

def wait_for_file(file_path, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(file_path):
            return True
        time.sleep(0.5)
    return False

def play_audio(audio_file):
    try:
        if not wait_for_file(audio_file):
            logger.error(f"Audio file not found after waiting: {audio_file}")
            return

        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        logger.info(f"Played audio file: {audio_file}")
    except Exception as e:
        logger.error(f"Error playing audio file: {str(e)}")

def main():
    logger.info("Starting the AI assistant...")
    
    try:
        while True:
            # Listen for wake word
            listen_for_wakeword()
            
            # Record audio
            audio_file = record_audio()
            
            # Transcribe audio
            transcription_file = transcribe_and_save(audio_file)
            
            # Process transcription and generate response
            response_audio_file = chat_interface_main(transcription_file)
            
            # Play the response audio if it was generated successfully
            if response_audio_file:
                logger.info(f"Playing audio response: {response_audio_file}")
                play_audio(response_audio_file)
                logger.info("Audio playback completed.")
            else:
                logger.warning("No audio response to play.")
            
            logger.info("Interaction complete. Waiting for next wake word...")
    
    except KeyboardInterrupt:
        logger.info("AI assistant interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        # Quit pygame mixer when the program ends
        pygame.mixer.quit()
    
    logger.info("AI assistant shutting down.")

if __name__ == "__main__":
    main()