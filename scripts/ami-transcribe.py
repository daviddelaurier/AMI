import os
import shutil
import time
import logging
from dotenv import load_dotenv
import pyaudio
import wave
import numpy as np
import keyboard
import torch
import gc
from colorama import init, Fore, Style
from datetime import datetime
import threading
from pydub import AudioSegment
from groq import Groq

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()

# Constants
WAKE_WORD = "hey amy"
SILENCE_THRESHOLD = 500
SILENCE_DURATION = 5
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
OUTPUT_PATH = os.getenv("GROQ_TEXT_OUTPUT")
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_PATH = os.getenv("MODEL_PATH", "models")

# Ensure output directory exists
os.makedirs(OUTPUT_PATH, exist_ok=True)
os.makedirs(MODEL_PATH, exist_ok=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_ascii_art():
    art = [
        " _ __ __ ___ ",
        " / \\ | \\/ | |_ _|",
        " / _ \\ | |\\/| | | | ",
        " / ___ \\| | | | | | ",
        "/_/ \\_\\_| |_| |___|",
    ]
    for line in art:
        print(Fore.CYAN + line)
        time.sleep(0.2)
    print(Style.RESET_ALL)

def list_input_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    devices = []
    for i in range(num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            devices.append({
                'index': i,
                'name': device_info.get('name')
            })
    p.terminate()
    return devices

def initialize_audio(device_index=None):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK_SIZE)
    return p, stream

def is_silent(audio_data, threshold):
    return np.max(np.abs(audio_data)) < threshold

def save_audio(frames, filename):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    logger.info(f"Audio saved to {filename}")
    print(Fore.GREEN + f"Audio saved to {filename}")

def record_audio(stream, append_to=None):
    print(Fore.YELLOW + "Recording... (Press 'q' to stop manually)")
    frames = []
    silence_start = None
    if append_to:
        existing_audio = AudioSegment.from_wav(append_to)
        frames = list(existing_audio.raw_data)

    while True:
        audio_data = stream.read(CHUNK_SIZE)
        frames.append(audio_data)

        if is_silent(np.frombuffer(audio_data, dtype=np.int16), SILENCE_THRESHOLD):
            if silence_start is None:
                silence_start = time.time()
            elif time.time() - silence_start > SILENCE_DURATION:
                break
        else:
            silence_start = None

        if keyboard.is_pressed('q'):
            print(Fore.YELLOW + "Manual stop triggered.")
            break

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(OUTPUT_PATH, f"recording_{timestamp}.wav")
    save_audio(frames, filename)
    return filename

def transcribe_audio(audio_file, model="whisper-large-v3", prompt=None, response_format="text", language=None, temperature=0.0):
    print(Fore.CYAN + f"Transcribing audio file: {audio_file}")
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
        print(Fore.RED + "Transcription failed. No result to save.")
        return None

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    transcription_file = os.path.join(OUTPUT_PATH, f"transcription_{timestamp}.txt")
    with open(transcription_file, 'w', encoding='utf-8') as f:
        if hasattr(result, 'text'):
            f.write(result.text)
        else:
            f.write(str(result))
    print(Fore.GREEN + f"Transcription saved to {transcription_file}")
    return transcription_file

def transcribe_in_background(audio_file):
    threading.Thread(target=transcribe_and_save, args=(audio_file,), daemon=True).start()

def transcribe_and_save(audio_file):
    result = transcribe_audio(audio_file)
    save_transcription(result, audio_file)

def combine_audio_files():
    print(Fore.YELLOW + "Combining all audio files in the output directory...")
    audio_files = [f for f in os.listdir(OUTPUT_PATH) if f.endswith('.wav')]
    if not audio_files:
        print(Fore.RED + "No audio files found in the output directory.")
        return

    combined = AudioSegment.empty()
    for audio_file in audio_files:
        combined += AudioSegment.from_wav(os.path.join(OUTPUT_PATH, audio_file))

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = os.path.join(OUTPUT_PATH, f"combined_audio_{timestamp}.wav")
    combined.export(output_file, format="wav")
    print(Fore.GREEN + f"Combined audio saved to {output_file}")

def main():
    print_ascii_art()
    print(Fore.MAGENTA + "A.M.I. Audio Recording and Transcription System")
    print(Fore.MAGENTA + "==============================================")

    # List available input devices
    devices = list_input_devices()
    print(Fore.CYAN + "Available input devices:")
    for device in devices:
        print(f"{device['index']}: {device['name']}")

    # Let the user select a device
    while True:
        try:
            device_index = int(input("Enter the number of the input device you want to use (or press Enter for default): "))
            if device_index in [device['index'] for device in devices]:
                break
            else:
                print(Fore.RED + "Invalid device number. Please try again.")
        except ValueError:
            device_index = None
            break

    p, stream = initialize_audio(device_index)

    try:
        print(Fore.CYAN + f"Listening for wake word: '{WAKE_WORD}'")
        print(Fore.CYAN + "Press 'r' to start recording manually")
        print(Fore.CYAN + "Press 'c' to combine all audio files")
        print(Fore.CYAN + "Press 'd' to change input device")
        print(Fore.CYAN + "Press 'q' to quit the program")

        last_recording = None

        while True:
            if keyboard.is_pressed('r'):
                print(Fore.YELLOW + "Manual recording triggered.")
                append_choice = input("Do you want to append to the last recording? (y/n): ").lower()
                if append_choice == 'y' and last_recording:
                    audio_file = record_audio(stream, append_to=last_recording)
                else:
                    audio_file = record_audio(stream)
                last_recording = audio_file
                transcribe_in_background(audio_file)
                continue_choice = input("Do you want to record another clip? (y/n): ").lower()
                if continue_choice != 'y':
                    break

            if keyboard.is_pressed('c'):
                combine_audio_files()

            if keyboard.is_pressed('d'):
                print(Fore.YELLOW + "Changing input device...")
                stream.stop_stream()
                stream.close()
                p.terminate()

                devices = list_input_devices()
                print(Fore.CYAN + "Available input devices:")
                for device in devices:
                    print(f"{device['index']}: {device['name']}")

                while True:
                    try:
                        device_index = int(input("Enter the number of the input device you want to use: "))
                        if device_index in [device['index'] for device in devices]:
                            break
                        else:
                            print(Fore.RED + "Invalid device number. Please try again.")
                    except ValueError:
                        print(Fore.RED + "Invalid input. Please enter a number.")

                p, stream = initialize_audio(device_index)
                print(Fore.GREEN + "Input device changed successfully.")

            if keyboard.is_pressed('q'):
                print(Fore.RED + "Quitting program...")
                break

    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram interrupted by user.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print(Fore.MAGENTA + "Audio recording and transcription system shut down.")

if __name__ == "__main__":
    main()