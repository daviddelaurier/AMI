import os
from dotenv import load_dotenv
import requests
from datetime import datetime
from tqdm import tqdm
import pyaudio
import wave
import logging
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
logger.info("Loading environment variables...")
load_dotenv()

# Constants
TRANSCRIPT = os.getenv("TRANSCRIPTION_OUTPUT")
OUTPUT_AUDIO_PATH = os.getenv("SPEECH_OUTPUT_PATH")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
logger.info(f"GROQ_API_KEY loaded: {'Yes' if GROQ_API_KEY else 'No'}")

os.makedirs(OUTPUT_AUDIO_PATH, exist_ok=True)
logger.info(f"TRANSCRIPT: {TRANSCRIPT}")
logger.info(f"OUTPUT_AUDIO_PATH: {OUTPUT_AUDIO_PATH}")

def read_text_files(directory):
    logger.info(f"Reading text files from directory: {directory}")
    text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    texts = []
    for file_name in text_files:
        file_path = os.path.join(directory, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            texts.append((file_name, text))
            logger.info(f"Read '{file_name}'. Length: {len(text)} characters")
        except Exception as e:
            logger.error(f"Error reading {file_name}: {str(e)}")
    return texts

def synthesize_speech(text, output_file):
    try:
        logger.info("Starting speech synthesis...")
        logger.info(f"Input text: '{text}'")
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"  # Voice ID for "Bella"
        
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        headers = {
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }

        logger.info("Sending request to ElevenLabs API...")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            logger.info(f"Saving synthesized speech to {output_file}")
            with open(output_file, "wb") as f:
                f.write(response.content)
            logger.info(f"Speech synthesized and saved successfully.")
            return True
        else:
            logger.error(f"Error from ElevenLabs API: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"An error occurred during speech synthesis: {str(e)}")
        return False

def play_audio(file_path):
    try:
        logger.info(f"Playing synthesized audio: {file_path}")
        
        # Open the audio file
        wf = wave.open(file_path, 'rb')
        
        # Initialize PyAudio
        p = pyaudio.PyAudio()
        
        # Open a stream
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        
        # Read data in chunks
        chunk_size = 1024
        data = wf.readframes(chunk_size)
        
        # Play the audio
        while data:
            stream.write(data)
            data = wf.readframes(chunk_size)
        
        # Clean up
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        logger.info("Audio playback completed.")
    except Exception as e:
        logger.error(f"Error playing audio: {str(e)}")

def process_text_with_groq(text):
    logger.info("Processing text with Groq API...")
    model = 'llama3-8b-8192'
    groq_chat = ChatGroq(groq_api_key=GROQ_API_KEY, model_name=model)
    
    system_prompt = 'You are a friendly conversational chatbot'
    memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)
    
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{human_input}")
    ])
    
    conversation = LLMChain(
        llm=groq_chat,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    
    response = conversation.predict(human_input=text)
    logger.info("Groq API processing completed.")
    return response

def main(transcription_file):
    try:
        logger.info("Starting main process...")
        
        # Read the transcription file
        with open(transcription_file, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Process text with Groq API
        processed_text = process_text_with_groq(text)
        
        # Generate a unique filename for the synthesized speech
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = os.path.join(OUTPUT_AUDIO_PATH, f"response_{timestamp}.mp3")
        logger.info(f"Processing transcription. Output file will be: {output_file}")
        
        # Synthesize speech
        success = synthesize_speech(processed_text, output_file)
        if success:
            logger.info(f"Speech synthesized successfully: {output_file}")
            return output_file
        else:
            logger.error("Speech synthesis failed.")
            return None
        
    except Exception as e:
        logger.error(f"An error occurred in the main process: {str(e)}")
        return None

if __name__ == "__main__":
    logger.info("Script started.")
    main()
    logger.info("Script finished.")