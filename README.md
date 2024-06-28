# myAI - AMI Voice Inference Module

![myAI Logo](https://example.com/myai-logo.png)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Future Improvements](#future-improvements)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

myAI - AMI Voice Inference Module is an advanced voice-controlled AI assistant designed to serve as the primary voice interface for an AI-integrated smart home ecosystem. This cutting-edge system combines state-of-the-art speech recognition, natural language processing, and text-to-speech capabilities to create a seamless and intuitive interaction between users and their AI-enhanced environment.

![AMI in action](https://example.com/ami-in-action.gif)

## Features

- 🎙️ Voice activation using the customizable wake phrase "Hey Amy"
- 🗣️ Advanced speech recognition for precise command interpretation
- 🧠 Integration with Anthropic's Claude AI for sophisticated natural language understanding and response generation
- 📝 Local speech-to-text transcription using OpenAI's Whisper model for enhanced privacy and reduced latency
- 🔊 Text-to-speech synthesis using the MARS5 model for natural and expressive vocal responses
- 🎵 Immersive audio feedback system for user interaction cues

## System Architecture

The myAI - AMI Voice Inference Module is built on a modular architecture that ensures scalability and ease of future enhancements.

![System Architecture Diagram](https://example.com/myai-architecture.png)

1. **Voice Activation Module**: Utilizes the SpeechRecognition library to continuously listen for the wake phrase.
2. **Command Recognition Module**: Processes user voice commands and prepares them for AI interpretation.
3. **Whisper Transcription Engine**: Converts spoken language to text using OpenAI's Whisper model.
4. **Claude AI Integration**: Leverages Anthropic's Claude for advanced natural language processing and response generation.
5. **MARS5 Text-to-Speech Engine**: Transforms AI-generated text responses into natural-sounding speech.
6. **Audio Playback System**: Manages system feedback and AI voice output through the computer's audio interface.

## Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended for optimal performance)
- Microphone and speakers/headphones
- Internet connection (for Claude AI integration)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/myai-ami-voice-inference.git
   cd myai-ami-voice-inference
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and add your Anthropic API key.

## Usage

To start the myAI - AMI Voice Inference Module:

```bash
python voice_inference.py
```

Once initiated, the system will await the activation phrase "Hey Amy". Upon activation, say "I have a question" to begin your query. To conclude your query, simply say "end recording".

![Usage Example](https://example.com/myai-usage-example.gif)

## Project Structure

```
myai-ami-voice-inference/
├── voice_inference.py
├── requirements.txt
├── .env
├── README.md
├── LICENSE
└── models/
    ├── whisper/
    └── mars5/
```

## Configuration

The system can be customized through the `.env` file:

- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude AI integration
- `DATABASE_DIRECTORY`: Location for storing interaction history
- `LOGS_DIRECTORY`: Directory for system logs

Additional configuration options can be found in the `config.py` file (not shown in the provided files).

## Future Improvements

The myAI - AMI Voice Inference Module is under active development. Planned enhancements include:

- 🖼️ Integration with Florence-2 Computer Vision model for visual scene understanding
- 🌐 Web search capabilities for real-time information retrieval
- 💻 Code execution features for advanced automation tasks
- 🏠 Expanded smart home device integration

## Troubleshooting

Common issues and their solutions:

| Issue | Solution |
|-------|----------|
| Microphone not detected | Ensure your microphone is properly connected and selected as the default input device |
| "Hey Amy" not recognized | Try adjusting your microphone volume or speaking more clearly |
| Slow response times | Check your internet connection or consider upgrading your GPU for faster processing |

For more detailed troubleshooting, please refer to our [Wiki](https://github.com/yourusername/myai-ami-voice-inference/wiki/Troubleshooting).

## Contributing

We welcome contributions to the myAI - AMI Voice Inference Module! Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Anthropic](https://www.anthropic.com) for the Claude AI model
- [OpenAI](https://openai.com) for the Whisper speech recognition model
- [Camb-ai](https://github.com/Camb-ai/mars5-tts) for the MARS5 text-to-speech model
- All our contributors and users who help improve this project

---

<p align="center">
  Made with ❤️ by the myAI Team
</p>

![Visitors](https://visitor-badge.glitch.me/badge?page_id=yourusername.myai-ami-voice-inference)
```
