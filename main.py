import os
from datetime import datetime
import pygame

def get_most_recent_file(directory):
    files = os.listdir(directory)
    if not files:
        return None
    
    return max(
        [os.path.join(directory, f) for f in files],
        key=os.path.getmtime
    )

def play_audio():
    audio_dir = os.path.join('data', 'speech_output')
    most_recent_file = get_most_recent_file(audio_dir)
    
    if most_recent_file:
        pygame.mixer.init()
        pygame.mixer.music.load(most_recent_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print("No audio files found in the directory.")