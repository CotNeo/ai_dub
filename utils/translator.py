"""
Translation module for AI Dubbing project.
This module handles text translation using Google Translate (unofficial) or OpenAI GPT.
"""

import os
import time
import json
import requests
from translatepy import Translator as TranslatePyTranslator
from config.settings import (
    TEMP_TRANSCRIPT_PATH, 
    TEMP_TRANSLATED_PATH, 
    SOURCE_LANGUAGE, 
    TARGET_LANGUAGE,
    TRANSLATION_ENGINE,
    OPENAI_API_KEY
)
from utils.logger import setup_logger

logger = setup_logger(__name__)

def translate_text_google(text, source_lang=SOURCE_LANGUAGE, target_lang=TARGET_LANGUAGE):
    """
    Translate text using Google Translate via translatepy.
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language code
        target_lang (str): Target language code
    
    Returns:
        str: Translated text
    """
    try:
        logger.info(f"Translating text using Google Translate ({source_lang} → {target_lang})")
        translator = TranslatePyTranslator()
        result = translator.translate(text, source_lang, target_lang)
        return result.result
    except Exception as e:
        logger.error(f"Error translating with Google: {str(e)}")
        return None

def translate_text_openai(text, source_lang=SOURCE_LANGUAGE, target_lang=TARGET_LANGUAGE):
    """
    Translate text using OpenAI's GPT model.
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language code
        target_lang (str): Target language code
    
    Returns:
        str: Translated text
    """
    if not OPENAI_API_KEY:
        logger.error("OpenAI API key not found. Please set it in settings.py or environment variables.")
        return None
        
    try:
        logger.info(f"Translating text using OpenAI GPT ({source_lang} → {target_lang})")
        
        # Prepare request to OpenAI API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        # Create system message for controlling translation behavior
        system_message = f"You are a professional translator. Translate the following text from {source_lang} to {target_lang}. Keep the text structure and formatting intact. Only return the translated text, no explanations or additional text."
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": text}
            ],
            "temperature": 0.3,  # Lower temperature for more consistent translations
            "max_tokens": 2048   # Adjust as needed
        }
        
        # Make API request
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        
        # Parse response
        response_data = response.json()
        if "choices" in response_data and len(response_data["choices"]) > 0:
            translated_text = response_data["choices"][0]["message"]["content"].strip()
            return translated_text
        else:
            logger.error(f"Unexpected response from OpenAI: {response_data}")
            return None
            
    except Exception as e:
        logger.error(f"Error translating with OpenAI: {str(e)}")
        return None

def translate_file(input_path=TEMP_TRANSCRIPT_PATH, output_path=TEMP_TRANSLATED_PATH,
                source_lang=SOURCE_LANGUAGE, target_lang=TARGET_LANGUAGE, 
                engine=TRANSLATION_ENGINE):
    """
    Translate text file from source language to target language.
    
    Args:
        input_path (str): Path to input text file
        output_path (str): Path to save translated text
        source_lang (str): Source language code
        target_lang (str): Target language code
        engine (str): Translation engine to use ('google' or 'openai')
    
    Returns:
        str: Path to translated file, or None if translation failed
    """
    logger.info(f"Translating file: {input_path} ({source_lang} → {target_lang}) using {engine}")
    
    # Check if input file exists
    if not os.path.exists(input_path):
        logger.error(f"Input file not found: {input_path}")
        return None
    
    try:
        # Read input file
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        logger.info(f"Loaded text from {input_path} ({len(text)} characters)")
        
        # Translate text based on selected engine
        start_time = time.time()
        
        if engine.lower() == "google":
            translated_text = translate_text_google(text, source_lang, target_lang)
        elif engine.lower() == "openai":
            translated_text = translate_text_openai(text, source_lang, target_lang)
        else:
            logger.error(f"Unknown translation engine: {engine}")
            return None
            
        if translated_text is None:
            logger.error("Translation failed")
            return None
            
        translation_time = time.time() - start_time
        logger.info(f"Translation completed in {translation_time:.2f} seconds")
        
        # Save translated text to output file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(translated_text)
            
        logger.info(f"Translated text saved to {output_path}")
        logger.info(f"Translation length: {len(translated_text)} characters")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error during translation: {str(e)}")
        return None


# Example usage
if __name__ == "__main__":
    # Test with a sample transcript file (assuming it exists)
    if os.path.exists(TEMP_TRANSCRIPT_PATH):
        translate_file()
    else:
        print(f"Test transcript not found at {TEMP_TRANSCRIPT_PATH}") 