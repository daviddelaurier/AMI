from dotenv import load_dotenv
import os
import pvporcupine
import pyaudio
import struct
from record_audio import record_audio
from transcription import transcribe_and_save
from chat_interface import main as chat_interface_main

load_dotenv()

ACCESS_KEY = os.getenv('ACCESS_KEY')
KEYWORD_PATH = os.getenv('KEYWORD_PATH')
TRANSCRIPTION_OUTPUT = os.getenv('TRANSCRIPTION_OUTPUT')

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

        print("Listening for 'Hey Amy'...")

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word detected!")
                recorded_file = record_audio()
                transcription_file = transcribe_and_save(recorded_file, TRANSCRIPTION_OUTPUT)
                chat_interface_main(transcription_file)
                print("Listening for 'Hey Amy'...")

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()

if __name__ == "__main__":
    listen_for_wakeword()