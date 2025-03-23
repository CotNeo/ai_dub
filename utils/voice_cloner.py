"""
Voice Cloning Module for AI Dub
This module provides functionality for cloning a speaker's voice and generating speech
in a target language using the Coqui TTS XTTS model.
"""

import os
import time
import torch
import logging
from TTS.tts.configs.xtts_config import XttsConfig

# Register the XTTS config as a safe global for PyTorch 2.6+
try:
    torch.serialization.add_safe_globals([XttsConfig])
except AttributeError:
    # PyTorch version doesn't have add_safe_globals (version < 2.6)
    pass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clone_voice_and_speak(text, speaker_wav_path, target_lang="en", output_path=None):
    """
    Clone a voice from an audio sample and generate speech in the target language.
    
    Args:
        text (str): The text to convert to speech
        speaker_wav_path (str): Path to the audio file containing the speaker's voice
        target_lang (str): Target language code (e.g., 'en', 'fr', 'tr')
        output_path (str, optional): Path to save the generated audio file
                                    If None, will generate a path
    
    Returns:
        str: Path to the generated audio file, or None if generation failed
    """
    start_time = time.time()
    
    # Log the start of the process
    logger.info(f"Starting XTTS voice cloning from sample: {speaker_wav_path}")
    logger.info(f"Target language: {target_lang}, Output path: {output_path}")
    
    # Verify the speaker's audio sample exists
    if not os.path.exists(speaker_wav_path):
        logger.error(f"Speaker audio sample not found: {speaker_wav_path}")
        return None
    
    # Generate output path if not provided
    if not output_path:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"xtts_cloned_{int(time.time())}.wav")
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Map language codes to XTTS format
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
    logger.info(f"Using language code '{xtts_lang}' for XTTS")
    
    # Check if GPU is available
    use_gpu = torch.cuda.is_available()
    logger.info(f"GPU acceleration: {'Enabled' if use_gpu else 'Disabled'}")
    
    try:
        from TTS.api import TTS
        
        # Initialize TTS with XTTS v2 model - use the higher-level API which handles PyTorch compatibility
        model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        tts = TTS(model_name=model_name, gpu=use_gpu)
        
        logger.info(f"Model loaded: {model_name}")
        
        # Generate speech with voice cloning
        logger.info("Generating speech with cloned voice...")
        tts.tts_to_file(
            text=text,
            file_path=output_path,
            speaker_wav=speaker_wav_path,
            language=xtts_lang
        )
        
        # Log performance metrics
        end_time = time.time()
        generation_time = end_time - start_time
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        
        logger.info(f"Voice cloning completed in {generation_time:.2f} seconds")
        logger.info(f"Generated audio saved to: {output_path} ({file_size_mb:.2f} MB)")
        
        return output_path
        
    except ImportError:
        logger.error("TTS library not installed. Install using 'pip install TTS'")
        return None
    except Exception as e:
        logger.error(f"Error in voice cloning: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Example text in multiple languages
    sample_text = "This is a test of the voice cloning system. The voice you're hearing has been cloned from a reference audio sample."
    
    # Path to a reference audio file (should be at least 3 seconds)
    reference_audio = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "outputs", "samples", "test_reference_audio.wav"
    )
    
    # Generate speech with the cloned voice
    output_path = clone_voice_and_speak(
        text=sample_text,
        speaker_wav_path=reference_audio,
        target_lang="en"
    )
    
    if output_path:
        print(f"Successfully generated cloned speech: {output_path}")
    else:
        print("Failed to generate cloned speech") 