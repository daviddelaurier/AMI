# Repository Structure

```
artificial-me-intelligence/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── components/
│   │       ├── __init__.py
│   │       ├── transcription.py
│   │       ├── speech_synthesis.py
│   │       └── chat_interface.py
│   │
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── transcription_service.py
│   │   ├── speech_synthesis_service.py
│   │   ├── chat_service.py
│   │   └── api_tracking.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── schema.py
│   │   └── db_manager.py
│   │
│   ├── obs_integration/
│   │   ├── __init__.py
│   │   ├── obs_controller.py
│   │   └── voice_control.py
│   │
│   ├── cloud_storage/
│   │   ├── __init__.py
│   │   ├── s3_manager.py
│   │   └── data_sync.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py
│       └── logger.py
│
├── tests/
│   ├── unit/
│   │   ├── test_transcription.py
│   │   ├── test_speech_synthesis.py
│   │   └── test_chat_service.py
│   │
│   └── integration/
│       ├── test_app.py
│       └── test_obs_integration.py
│
├── scripts/
│   ├── setup_database.py
│   └── generate_test_data.py
│
├── docs/
│   ├── api_documentation.md
│   ├── user_guide.md
│   └── developer_guide.md
│
├── static/
│   ├── css/
│   │   └── custom_styles.css
│   ├── js/
│   │   └── custom_scripts.js
│   └── images/
│       └── logo.png
│
├── .gitignore
├── README.md
├── requirements.txt
├── setup.py
└── Dockerfile
```