import speech_recognition as sr
import pyaudio
import wave
import whisper
import anthropic
import torch
import librosa
import sounddevice as sd
import os
import numpy as np

def generate_tone(frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(frequency * t * 2 * np.pi)
    return tone.astype(np.float32)

def play_tone(frequency, duration):
    audio = generate_tone(frequency, duration)
    sd.play(audio, samplerate=44100)
    sd.wait()

def play_activation_tone():
    play_tone(800, 0.3)  # 800 Hz for 0.3 seconds

def play_end_recording_tone():
    play_tone(600, 0.3)  # 600 Hz for 0.3 seconds

def listen_for_activation_phrase():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'Hey Amy'...")
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio).lower()
                if "hey amy" in text:
                    print("Activation phrase detected!")
                    play_activation_tone()
                    return True
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Could not request results; check your network connection")

def listen_for_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for 'I have a question'...")
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio).lower()
                if "i have a question" in text:
                    print("Command recognized!")
                    return True
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Could not request results; check your network connection")

def check_for_end_recording_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, phrase_time_limit=2)  # Listen for up to 2 seconds
        try:
            text = recognizer.recognize_google(audio).lower()
            return "end recording" in text
        except sr.UnknownValueError:
            return False
        except sr.RequestError:
            print("Could not request results; check your network connection")
            return False

def record_voice_message():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("\033[91mRECORDING\033[0m")
    frames = []

    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        if check_for_end_recording_command():
            break

    print("Finished recording")
    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames, RATE

def end_recording_and_save_voice_message(frames, RATE):
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    play_end_recording_tone()

def initialize_whisper_model():
    global whisper_model
    whisper_model = whisper.load_model("base")

def transcribe_voice_message_using_whisper_locally():
    global whisper_model
    result = whisper_model.transcribe("output.wav")
    return result["text"]

def send_transcribed_text_file_to_anthropic_api(transcribed_text):
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": transcribed_text}
        ]
    )
    return message.content

def initialize_mars5_model():
    global mars5, config_class
    mars5, config_class = torch.hub.load('Camb-ai/mars5-tts', 'mars5_english', trust_repo=True)

def generate_amis_voice_response_with_MARS5_locally(text, ref_audio_path, ref_transcript):
    global mars5, config_class
    wav, sr = librosa.load(ref_audio_path, sr=mars5.sr, mono=True)
    wav = torch.from_numpy(wav)

    cfg = config_class(deep_clone=True, rep_penalty_window=100,
                       top_k=100, temperature=0.7, freq_penalty=3)

    _, output_audio = mars5.tts(text, wav, ref_transcript, cfg=cfg)
    
    return output_audio

def play_amis_voice_response_through_computer_audio_out(audio, sample_rate=24000):
    sd.play(audio, sample_rate)
    sd.wait()

def main_voice_controlled_ai_assistant_loop():
    initialize_whisper_model()
    initialize_mars5_model()

    while True:
        if listen_for_activation_phrase():
            if listen_for_voice_command():
                frames, rate = record_voice_message()
                end_recording_and_save_voice_message(frames, rate)
                
                transcribed_text = transcribe_voice_message_using_whisper_locally()
                anthropic_response = send_transcribed_text_file_to_anthropic_api(transcribed_text)
                
                ami_voice = generate_amis_voice_response_with_MARS5_locally(
                    anthropic_response, 
                    "<path to reference audio>",
                    "<reference transcript>"
                )
                play_amis_voice_response_through_computer_audio_out(ami_voice)

if __name__ == "__main__":
    main_voice_controlled_ai_assistant_loop()