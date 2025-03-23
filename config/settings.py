"""
Configuration settings for the AI Dubbing project.
This file contains all configurable parameters including API keys, language settings,
and directory configurations.
"""

import os
from pathlib import Path

# Base directory paths
BASE_DIR = Path(__file__).parent.parent
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Create required directories if they don't exist
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Temporary file paths
TEMP_VIDEO_PATH = os.path.join(OUTPUTS_DIR, "temp_video.mp4")
TEMP_AUDIO_PATH = os.path.join(OUTPUTS_DIR, "temp_audio.wav")
TEMP_TRANSCRIPT_PATH = os.path.join(OUTPUTS_DIR, "transcript.txt")
TEMP_TRANSLATED_PATH = os.path.join(OUTPUTS_DIR, "translated.txt")
TEMP_DUBBED_AUDIO_PATH = os.path.join(OUTPUTS_DIR, "dubbed_audio.wav")
OUTPUT_VIDEO_PATH = os.path.join(OUTPUTS_DIR, "dubbed_video.mp4")

# Language settings
SOURCE_LANGUAGE = "en"  # Default source language
TARGET_LANGUAGE = "tr"  # Default target language

# Try to import API keys from api_keys.py, fall back to environment variables
try:
    from config.api_keys import OPENAI_API_KEY
except ImportError:
    # API keys (replace with your actual keys if needed)
    # It's better to use environment variables in production
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Whisper settings
WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large

# TTS settings 
TTS_ENGINE = "gtts"  # Options: bark, coqui, gtts, voice_clone

# Reference audio for voice cloning (if TTS_ENGINE is voice_clone)
REFERENCE_AUDIO_PATH = os.path.join(OUTPUTS_DIR, "reference_audio.wav")

# Translation settings
TRANSLATION_ENGINE = "google"  # Options: google, openai

# Log settings
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(LOGS_DIR, "process.log") 