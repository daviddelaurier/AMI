import logging

from dotenv import load_dotenv
from components.record_audio import record_audio
from components.transcription import transcribe_and_save
from components.listen_for_wakeword import listen_for_wakeword
from components.chat_interface import main as chat_interface_main

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting the AI assistant...")
    
    while True:
        try:
            # Listen for wake word
            listen_for_wakeword()
            
            # Record audio
            audio_file = record_audio()
            
            # Transcribe audio
            transcription_file = transcribe_and_save(audio_file)
            
            # Process transcription and generate response
            chat_interface_main(transcription_file)
            
            logger.info("Waiting for next interaction...")
        
        except KeyboardInterrupt:
            logger.info("Shutting down the AI assistant...")
            break
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            logger.info("Restarting the main loop...")

if __name__ == "__main__":
    main()