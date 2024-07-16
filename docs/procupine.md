Porcupine Wake Word
Python Quick Start
Platforms
Linux (x86_64)
macOS (x86_64, arm64)
Windows (x86_64)
BeagleBone
NVIDIA Jetson Nano
Raspberry Pi (Zero, 2, 3, 4, 5)
Requirements
Picovoice Account & AccessKey
Python 3.7+
PIP
Picovoice Account & AccessKey
Signup or Login to Picovoice Console to get your AccessKey. Make sure to keep your AccessKey secret.

Quick Start
Setup
Install Python 3 .

Install the pvporcupine Python package  using PIP:

pip3 install pvporcupine
Usage
Create an instance of Porcupine Wake Word that detects the included built-in wake words porcupine and bumblebee:

import pvporcupine

porcupine = pvporcupine.create(
  access_key='${ACCESS_KEY}',
  keywords=['picovoice', 'bumblebee']
)
Pass in frames of audio to the .process function:

def get_next_audio_frame():
  pass

while True:
  audio_frame = get_next_audio_frame()
  keyword_index = porcupine.process(audio_frame)
  if keyword_index == 0:
      # detected `porcupine`
  elif keyword_index == 1:
      # detected `bumblebee`
Release resources explicitly when done with Porcupine Wake Word:

porcupine.delete()
Custom Keywords
Create custom keywords using the Picovoice Console. Download the custom wake word file (.ppn) and create an instance of Porcupine Wake Word using the keyword_paths input argument:

porcupine = pvporcupine.create(
  access_key='${ACCESS_KEY}',
  keyword_paths=['${KEYWORD_FILE_PATH}']
)
Non-English Languages
Use the corresponding model file (.pv) to detect non-English wake words. The model files for all supported languages are available on the Porcupine Wake Word GitHub repository .

Pass in the model file using the model_path input argument to change the detection language:

porcupine = pvporcupine.create(
  access_key='${ACCESS_KEY}',
  keyword_paths=['${KEYWORD_FILE_PATH}'],
  model_path='${MODEL_FILE_PATH}'
)
Demo
For the Porcupine Wake Word Python SDK, we offer demo applications that demonstrate how to use the wake word engine on real-time audio streams (i.e. microphone input) and audio files.

Setup
Install the pvporcupinedemo Python package  using PIP:

pip3 install pvporcupinedemo
This package installs command-line utilities for the Porcupine Wake Word Python demos.

Usage
Use the --help flag to see the usage options for the demo:

porcupine_demo_mic --help
Ensure you have a working microphone connected to your system and run the following command to detect the built-in keyword porcupine:

Copy
porcupine_demo_mic --access_key ${ACCESS_KEY} --keywords porcupine