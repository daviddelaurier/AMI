import os
from dotenv import load_dotenv
import requests
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime
from tqdm import tqdm

# Load environment variables
print("Loading environment variables...")
load_dotenv()

# Constants
TRANSCRIPT = os.getenv("TRANSCRIPTION_OUTPUT")
OUTPUT_AUDIO_PATH = os.getenv("SPEECH_OUTPUT_PATH")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

os.makedirs(OUTPUT_AUDIO_PATH, exist_ok=True)
print(f"TRANSCRIPT: {TRANSCRIPT}")
print(f"OUTPUT_AUDIO_PATH: {OUTPUT_AUDIO_PATH}")

def read_text_files(directory):
    print(f"Reading text files from directory: {directory}")
    text_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    texts = []
    for file_name in text_files:
        file_path = os.path.join(directory, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            texts.append((file_name, text))
            print(f"Read '{file_name}'. Length: {len(text)} characters")
        except Exception as e:
            print(f"Error reading {file_name}: {str(e)}")
    return texts

def synthesize_speech(text, output_file):
    try:
        print("Starting speech synthesis...")
        print(f"Input text: '{text}'")
        
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

        print("Sending request to ElevenLabs API...")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"Saving synthesized speech to {output_file}")
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"Speech synthesized and saved successfully.")
            return True
        else:
            print(f"Error from ElevenLabs API: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"An error occurred during speech synthesis: {str(e)}")
        return False

def play_audio(file_path):
    try:
        print(f"Loading audio file: {file_path}")
        audio = AudioSegment.from_mp3(file_path)
        print(f"Playing audio: {file_path}")
        play(audio)
        print("Audio playback completed.")
    except Exception as e:
        print(f"Error playing audio: {str(e)}")

def main():
    try:
        print("Starting main process...")
        
        print("Reading input text files...")
        text_files = read_text_files(TRANSCRIPT)
        if not text_files:
            print("No text files found. Exiting.")
            return
        
        for file_name, text in text_files:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            output_file = os.path.join(OUTPUT_AUDIO_PATH, f"{file_name[:-4]}_{timestamp}.mp3")
            print(f"Processing '{file_name}'. Output file will be: {output_file}")
            
            success = synthesize_speech(text, output_file)
            if success:
                play_audio(output_file)
            else:
                print(f"Speech synthesis failed for '{file_name}'. Skipping audio playback.")
        
        print("Main process completed.")
    except Exception as e:
        print(f"An error occurred in the main process: {str(e)}")

if __name__ == "__main__":
    print("Script started.")
    main()
    print("Script finished.")