import logging
from functools import wraps
from google.cloud import speech, texttospeech
from src.database.db import insert_api_call

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a'
)

logger = logging.getLogger(__name__)

def handle_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            raise
    return wrapper

@handle_error
def transcribe_audio(audio_file):
    client = speech.SpeechClient()
    
    with open(audio_file, "rb") as audio_file:
        content = audio_file.read()
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    
    response = client.recognize(config=config, audio=audio)
    
    return response.results[0].alternatives[0].transcript if response.results else ""

@handle_error
def synthesize_speech(text):
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    output_file = "output.mp3"
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    
    return output_file

def track_api_call(system_message, user_message, transcription, image_filename, user_audio_filename, synthesized_audio_filename):
    insert_api_call(
        system_message=system_message,
        user_message=user_message,
        transcription=transcription,
        image_filename=image_filename,
        image_data=None,  # Implement image to base64 conversion if needed
        user_audio_filename=user_audio_filename,
        synthesized_audio_filename=synthesized_audio_filename
    )