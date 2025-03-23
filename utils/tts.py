"""
Text-to-Speech module for AI Dubbing project.
This module handles text-to-speech conversion using Bark, Coqui TTS, or Google TTS.
"""

import os
import time
import numpy as np
import soundfile as sf
from gtts import gTTS
from config.settings import (
    TEMP_TRANSLATED_PATH,
    TEMP_DUBBED_AUDIO_PATH,
    TARGET_LANGUAGE, 
    TTS_ENGINE
)
from utils.logger import setup_logger

logger = setup_logger(__name__)

def generate_speech_bark(text, output_path, language=TARGET_LANGUAGE, voice_preset="v2/en_speaker_6"):
    """
    Generate speech from text using Bark TTS (high quality but resource intensive).
    
    Args:
        text (str): Text to convert to speech
        output_path (str): Path to save the generated audio
        language (str): Language code
        voice_preset (str): Voice preset to use
    
    Returns:
        str: Path to the generated audio file, or None if generation failed
    """
    try:
        from bark import SAMPLE_RATE, generate_audio, preload_models
        
        # Adjust voice preset based on language
        if language.startswith("tr"):
            voice_preset = "v2/tr_speaker_0"  # Turkish speaker
        elif language.startswith("fr"):
            voice_preset = "v2/fr_speaker_0"  # French speaker
        elif language.startswith("es"):
            voice_preset = "v2/es_speaker_0"  # Spanish speaker
        elif language.startswith("de"):
            voice_preset = "v2/de_speaker_0"  # German speaker
        
        logger.info(f"Generating speech using Bark TTS (voice: {voice_preset})")
        
        # Preload models (one-time operation)
        preload_models()
        
        # Generate audio
        start_time = time.time()
        audio_array = generate_audio(text, history_prompt=voice_preset)
        
        # Save audio to disk
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        sf.write(output_path, audio_array, SAMPLE_RATE)
        
        generation_time = time.time() - start_time
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert to MB
        
        logger.info(f"Speech generated successfully to {output_path}")
        logger.info(f"Generation time: {generation_time:.2f} seconds, Size: {file_size:.2f} MB")
        
        return output_path
        
    except ImportError:
        logger.error("Bark TTS not installed. Install using 'pip install git+https://github.com/suno-ai/bark.git'")
        return None
    except Exception as e:
        logger.error(f"Error generating speech with Bark: {str(e)}")
        return None

def generate_speech_coqui(text, output_path, language=TARGET_LANGUAGE):
    """
    Generate speech from text using Coqui TTS (good quality, moderate resource usage).
    
    Args:
        text (str): Text to convert to speech
        output_path (str): Path to save the generated audio
        language (str): Language code
    
    Returns:
        str: Path to the generated audio file, or None if generation failed
    """
    try:
        from TTS.api import TTS
        
        logger.info("Generating speech using Coqui TTS")
        
        # Initialize TTS with appropriate model for language
        start_time = time.time()
        tts = TTS("tts_models/multilingual/multi-dataset/your_tts", gpu=True)
        
        # Generate speech
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        tts.tts_to_file(text=text, file_path=output_path)
        
        generation_time = time.time() - start_time
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert to MB
        
        logger.info(f"Speech generated successfully to {output_path}")
        logger.info(f"Generation time: {generation_time:.2f} seconds, Size: {file_size:.2f} MB")
        
        return output_path
        
    except ImportError:
        logger.error("Coqui TTS not installed. Install using 'pip install TTS'")
        return None
    except Exception as e:
        logger.error(f"Error generating speech with Coqui TTS: {str(e)}")
        return None

def generate_speech_voice_clone(text, output_path, reference_audio_path, language=TARGET_LANGUAGE):
    """
    Generate speech from text using Coqui YourTTS with voice cloning.
    
    Args:
        text (str): Text to convert to speech
        output_path (str): Path to save the generated audio
        reference_audio_path (str): Path to the reference audio for voice cloning
        language (str): Language code
    
    Returns:
        str: Path to the generated audio file, or None if generation failed
    """
    try:
        from TTS.api import TTS
        
        logger.info(f"Generating speech using voice cloning with reference: {reference_audio_path}")
        
        # Check if reference audio exists
        if not os.path.exists(reference_audio_path):
            logger.error(f"Reference audio file not found: {reference_audio_path}")
            return None
            
        # Map language codes to YourTTS format
        lang_mapping = {
            "en": "en",
            "tr": "en",  # YourTTS doesn't support Turkish, falling back to English
            "fr": "fr-fr",  # YourTTS uses fr-fr for French
            "es": "en",  # YourTTS doesn't support Spanish, falling back to English
            "de": "en",  # YourTTS doesn't support German, falling back to English
            "ru": "en",  # YourTTS doesn't support Russian, falling back to English
            "zh": "en",  # YourTTS doesn't support Chinese, falling back to English
            "ja": "en",  # YourTTS doesn't support Japanese, falling back to English
            "ko": "en",  # YourTTS doesn't support Korean, falling back to English
            "ar": "en",  # YourTTS doesn't support Arabic, falling back to English
            "pt": "pt-br"  # YourTTS uses pt-br for Brazilian Portuguese
        }
        
        # Get appropriate language code
        if language in lang_mapping:
            tts_lang = lang_mapping[language]
        elif language[:2] in lang_mapping:
            tts_lang = lang_mapping[language[:2]]
        else:
            tts_lang = "en"  # Default to English if language not found
            logger.warning(f"Language {language} not found in mapping, defaulting to English")
        
        logger.info(f"Using language code '{tts_lang}' for YourTTS voice cloning")
        
        # Initialize TTS with YourTTS model (optimized for voice cloning)
        start_time = time.time()
        tts = TTS("tts_models/multilingual/multi-dataset/your_tts")
        
        # Generate speech with voice cloning
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        logger.info(f"Starting voice cloning generation with language: {tts_lang}")
        
        tts.tts_to_file(
            text=text,
            file_path=output_path,
            speaker_wav=reference_audio_path,
            language=tts_lang
        )
        
        generation_time = time.time() - start_time
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert to MB
        
        logger.info(f"Voice cloned speech generated successfully to {output_path}")
        logger.info(f"Generation time: {generation_time:.2f} seconds, Size: {file_size:.2f} MB")
        
        return output_path
        
    except ImportError:
        logger.error("Coqui TTS not installed. Install using 'pip install TTS'")
        return None
    except Exception as e:
        logger.error(f"Error generating speech with voice cloning: {str(e)}")
        return None

def generate_speech_gtts(text, output_path, language=TARGET_LANGUAGE):
    """
    Generate speech from text using Google TTS (lower quality but very reliable).
    
    Args:
        text (str): Text to convert to speech
        output_path (str): Path to save the generated audio
        language (str): Language code
    
    Returns:
        str: Path to the generated audio file, or None if generation failed
    """
    try:
        logger.info(f"Generating speech using Google TTS (language: {language})")
        
        # Map language codes to Google TTS format if needed
        lang_mapping = {
            "en": "en",
            "tr": "tr",
            "fr": "fr",
            "es": "es",
            "de": "de",
            "ru": "ru",
            "zh": "zh-CN",
            "ja": "ja",
            "ko": "ko",
            "ar": "ar"
        }
        
        # Get appropriate language code
        if language in lang_mapping:
            tts_lang = lang_mapping[language]
        elif language[:2] in lang_mapping:
            tts_lang = lang_mapping[language[:2]]
        else:
            tts_lang = "en"  # Default to English if language not found
            logger.warning(f"Language {language} not found in mapping, defaulting to English")
        
        # Generate speech
        start_time = time.time()
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        
        # Save to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        tts.save(output_path)
        
        generation_time = time.time() - start_time
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert to MB
        
        logger.info(f"Speech generated successfully to {output_path}")
        logger.info(f"Generation time: {generation_time:.2f} seconds, Size: {file_size:.2f} MB")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error generating speech with Google TTS: {str(e)}")
        return None

def text_to_speech(input_path=TEMP_TRANSLATED_PATH, output_path=TEMP_DUBBED_AUDIO_PATH,
                 language=TARGET_LANGUAGE, engine=TTS_ENGINE, reference_audio=None):
    """
    Convert text from a file to speech using the specified TTS engine.
    
    Args:
        input_path (str): Path to the input text file
        output_path (str): Path to save the generated audio
        language (str): Language code
        engine (str): TTS engine to use ('bark', 'coqui', 'voice_clone', or 'gtts')
        reference_audio (str): Path to reference audio for voice cloning (only used if engine='voice_clone')
    
    Returns:
        str: Path to the generated audio file, or None if generation failed
    """
    logger.info(f"Converting text to speech: {input_path} using {engine} engine")
    
    # Check if input file exists
    if not os.path.exists(input_path):
        logger.error(f"Input file not found: {input_path}")
        return None
    
    try:
        # Read input file
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        logger.info(f"Loaded text from {input_path} ({len(text)} characters)")
        
        # Generate speech based on selected engine
        if engine.lower() == "bark":
            return generate_speech_bark(text, output_path, language)
        elif engine.lower() == "coqui":
            return generate_speech_coqui(text, output_path, language)
        elif engine.lower() == "gtts":
            return generate_speech_gtts(text, output_path, language)
        elif engine.lower() == "voice_clone":
            if reference_audio and os.path.exists(reference_audio):
                return generate_speech_voice_clone(text, output_path, reference_audio, language)
            else:
                logger.error(f"Voice cloning requires a valid reference audio file. Falling back to Google TTS.")
                return generate_speech_gtts(text, output_path, language)
        else:
            logger.error(f"Unknown TTS engine: {engine}")
            # Fall back to Google TTS if unknown engine
            logger.info("Falling back to Google TTS")
            return generate_speech_gtts(text, output_path, language)
            
    except Exception as e:
        logger.error(f"Error during text-to-speech conversion: {str(e)}")
        return None


# Example usage
if __name__ == "__main__":
    # Test with a sample translated file (assuming it exists)
    if os.path.exists(TEMP_TRANSLATED_PATH):
        text_to_speech()
    else:
        print(f"Test translation not found at {TEMP_TRANSLATED_PATH}") 