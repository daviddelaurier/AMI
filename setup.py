from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="AMI",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        "aiofiles>=23.2.1",
        "aiohttp>=3.9.5",
        "fastapi>=0.111.1",
        "gradio>=4.38.1",
        "langchain>=0.2.8",
        "numpy>=1.26.4",
        "openai>=1.35.14",
        "pandas>=2.2.2",
        "pillow>=10.4.0",
        "pydantic>=2.8.2",
        "PyAudio>=0.2.14",
        "python-dotenv>=1.0.1",
        "requests>=2.32.3",
        "SQLAlchemy>=2.0.31",
        "torch>=2.3.1",
        "torchaudio>=2.3.1",
        "torchvision>=0.18.1",
        "uvicorn>=0.30.1",
    ],
    author="David DeLaurier",
    author_email="datadelaurier@gmail.com",
    description="Artificial Me Intelligence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daviddelaurier/ami",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: Apache 2.0",
        "Operating System :: Windows 11",
        "Programming Language :: Python :: 3.10",

    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "ami=ami.cli:main",
        ],
    },
)