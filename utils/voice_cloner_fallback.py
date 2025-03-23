"""
Voice Cloning Module (Fallback Version)
This module provides alternatives when the XTTS model can't be loaded
due to compatibility issues.
"""

import os
import time
import logging
import torch
from gtts import gTTS
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clone_voice_fallback(text, target_lang="en", output_path=None):
    """
    A fallback method for generating speech when voice cloning fails.
    Uses gTTS (Google Text-to-Speech) as an alternative.
    
    Args:
        text (str): The text to convert to speech
        target_lang (str): Target language code (e.g., 'en', 'fr', 'tr')
        output_path (str, optional): Path to save the generated audio file.
                                    If None, will generate a path.
    
    Returns:
        str: Path to the generated audio file, or None if generation failed
    """
    start_time = time.time()
    
    # Log the start of the process
    logger.info(f"Starting fallback TTS for language: {target_lang}")
    logger.info(f"Output path: {output_path}")
    
    # Generate output path if not provided
    if not output_path:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"gtts_{int(time.time())}.mp3")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Map language codes to gTTS format
    lang_mapping = {
        "en": "en",
        "fr": "fr",
        "tr": "tr",
        "es": "es",
        "it": "it",
        "de": "de",
        "pt": "pt",
        "pl": "pl",
        "ru": "ru",
        "nl": "nl",
        "cs": "cs",
        "ar": "ar",
        "zh": "zh-CN",
        "ja": "ja",
        "ko": "ko",
        "hu": "hu"
    }
    
    # Get the gTTS language code
    gtts_lang = lang_mapping.get(target_lang.lower(), "en")
    logger.info(f"Using language code '{gtts_lang}' for gTTS")
    
    try:
        # Generate speech using gTTS
        logger.info("Generating speech with gTTS...")
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        tts.save(output_path)
        
        # Log performance metrics
        end_time = time.time()
        generation_time = end_time - start_time
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        
        logger.info(f"Speech generation completed in {generation_time:.2f} seconds")
        logger.info(f"Generated audio saved to: {output_path} ({file_size_mb:.2f} MB)")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error in fallback speech generation: {str(e)}")
        return None

def clone_voice_and_speak(text, speaker_wav_path=None, target_lang="en", output_path=None):
    """
    Try to clone a voice from an audio sample, falling back to gTTS if that fails.
    
    Args:
        text (str): The text to convert to speech
        speaker_wav_path (str, optional): Path to the audio file containing the speaker's voice
                                         (Not used in fallback mode)
        target_lang (str): Target language code (e.g., 'en', 'fr', 'tr')
        output_path (str, optional): Path to save the generated audio file
    
    Returns:
        str: Path to the generated audio file, or None if generation failed
    """
    logger.info("Attempting to generate speech using fallback method...")
    
    # Try the initial strategy first
    try:
        from TTS.api import TTS
        import torch
        
        # Check if the environment variable is set for PyTorch 2.6+ compatibility
        os.environ["TORCH_FULL_LOAD"] = "1"
        
        logger.info(f"Using PyTorch {torch.__version__}")
        logger.info(f"Attempting to load XTTS model...")
        
        # Try to initialize the TTS with voice cloning model
        if torch.cuda.is_available():
            logger.info("GPU is available, using CUDA")
            device = "cuda"
        else:
            logger.info("GPU not available, using CPU")
            device = "cpu"
        
        model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        
        # If speaker_wav_path is valid, attempt voice cloning
        if speaker_wav_path and os.path.exists(speaker_wav_path):
            try:
                # Use PyTorch 2.6+ compatible way to load the model
                tts = TTS(model_name=model_name, gpu=(device == "cuda"))
                
                # Map language codes
                lang_mapping = {
                    "en": "en",
                    "fr": "fr",
                    "tr": "tr",
                    "es": "es",
                    "it": "it",
                    "de": "de",
                    "pt": "pt",
                    "pl": "pl",
                    "ru": "ru",
                    "nl": "nl",
                    "cs": "cs",
                    "ar": "ar",
                    "zh": "zh-cn",
                    "ja": "ja",
                    "ko": "ko",
                    "hu": "hu"
                }
                
                # Get the XTTS language code
                xtts_lang = lang_mapping.get(target_lang.lower(), "en")
                
                # Generate speech with voice cloning
                tts.tts_to_file(
                    text=text,
                    file_path=output_path,
                    speaker_wav=speaker_wav_path,
                    language=xtts_lang
                )
                
                logger.info(f"XTTS voice cloning successful: {output_path}")
                return output_path
                
            except Exception as e:
                logger.warning(f"XTTS voice cloning failed: {str(e)}")
                logger.info("Falling back to gTTS...")
        
    except Exception as e:
        logger.warning(f"Could not initialize TTS model: {str(e)}")
        logger.info("Falling back to gTTS...")
    
    # Fallback to gTTS
    return clone_voice_fallback(text, target_lang, output_path)

# Example usage
if __name__ == "__main__":
    # Example text in multiple languages
    sample_text = "This is a test of the fallback TTS system. Due to compatibility issues, we're using an alternative speech synthesis approach."
    
    # Generate speech with the fallback method
    output_path = clone_voice_and_speak(
        text=sample_text,
        target_lang="en",
        output_path="outputs/fallback_en.mp3"
    )
    
    if output_path:
        print(f"Successfully generated speech: {output_path}")
    else:
        print("Failed to generate speech") 