"""
Transcription module for AI Dubbing project.
This module handles speech-to-text conversion using OpenAI's Whisper model.
"""

import os
import time
import whisper
from config.settings import TEMP_AUDIO_PATH, TEMP_TRANSCRIPT_PATH, WHISPER_MODEL, SOURCE_LANGUAGE
from utils.logger import setup_logger

logger = setup_logger(__name__)

def transcribe_audio(audio_path=TEMP_AUDIO_PATH, output_path=TEMP_TRANSCRIPT_PATH, 
                   model_name=WHISPER_MODEL, language=SOURCE_LANGUAGE):
    """
    Transcribe audio file to text using OpenAI's Whisper model.
    
    Args:
        audio_path (str): Path to the input audio file
        output_path (str): Path to save the transcript text file
        model_name (str): Whisper model size (tiny, base, small, medium, large)
        language (str): Language code for the audio (en, es, fr, etc.)
    
    Returns:
        str: Path to the transcript file, or None if transcription failed
    """
    logger.info(f"Transcribing audio: {audio_path} using Whisper {model_name} model")
    
    # Check if audio file exists
    if not os.path.exists(audio_path):
        logger.error(f"Audio file not found: {audio_path}")
        return None
    
    try:
        # Load the Whisper model
        start_time = time.time()
        logger.info(f"Loading Whisper {model_name} model...")
        model = whisper.load_model(model_name)
        logger.info(f"Model loaded in {time.time() - start_time:.2f} seconds")
        
        # Transcribe the audio
        logger.info("Starting transcription...")
        transcription_start = time.time()
        
        # Set transcription options
        options = {}
        if language:
            options["language"] = language
        
        # Perform transcription
        result = model.transcribe(audio_path, **options)
        
        transcription_time = time.time() - transcription_start
        logger.info(f"Transcription completed in {transcription_time:.2f} seconds")
        
        # Extract the transcribed text
        transcript = result["text"]
        
        # Save transcription to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        
        logger.info(f"Transcript saved to {output_path}")
        logger.info(f"Transcript length: {len(transcript)} characters")
        
        return output_path
    
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
        return None


# Example usage
if __name__ == "__main__":
    # Test with a sample audio file (assuming it exists)
    if os.path.exists(TEMP_AUDIO_PATH):
        transcribe_audio()
    else:
        print(f"Test audio not found at {TEMP_AUDIO_PATH}") 