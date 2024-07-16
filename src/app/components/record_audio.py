import os
from dotenv import load_dotenv
from datetime import datetime
import time
import torchaudio

# Load environment variables
load_dotenv()

# Constants
SAMPLE_RATE = 16000
CHANNELS = 1
RECORDING_DURATION = 5
AUDIO_RECORDING_OUTPUT = os.getenv('AUDIO_RECORDING_OUTPUT')

def record_audio():
    print(f"Recording audio for {RECORDING_DURATION} seconds...")
    
    # Initialize the audio recorder
    recorder = torchaudio.io.AudioRecorder(
        sample_rate=SAMPLE_RATE,
        num_channels=CHANNELS,
        format="wav"
    )

    # Start recording
    recorder.start()
    time.sleep(RECORDING_DURATION)
    recorder.stop()

    # Get the recorded audio
    waveform, _ = recorder.get_recorded()

    # Generate a unique filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"recording_{timestamp}.wav"
    file_path = os.path.join(AUDIO_RECORDING_OUTPUT, filename)

    # Save the audio file
    torchaudio.save(file_path, waveform, SAMPLE_RATE)
    print(f"Audio saved to: {file_path}")

    return file_path

def play_audio(file_path):
    print(f"Playing audio: {file_path}")
    waveform, sample_rate = torchaudio.load(file_path)
    torchaudio.play(waveform, sample_rate)
    print("Audio playback completed.")

if __name__ == "__main__":
    os.makedirs(AUDIO_RECORDING_OUTPUT, exist_ok=True)
    
    recorded_file = record_audio()
    play_audio(recorded_file)