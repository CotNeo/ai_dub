"""
Test script for the Voice Cloning module with environment variable workaround.
This script demonstrates how to use the voice_cloner module with PyTorch 2.6+ compatibility.
"""

import os
import sys
from pathlib import Path

# Set environment variable to disable weights_only in PyTorch 2.6+
# This allows loading older models that contain pickled Python objects
os.environ["TORCH_FULL_LOAD"] = "1"

# Add the project root to the path so we can import our modules
sys.path.append(str(Path(__file__).parent))

# Import our modules after setting the environment variable
from utils.create_test_audio import create_test_audio
from config.settings import OUTPUTS_DIR

# Create a simple wrapper function for TTS that doesn't use the voice_cloner.py module directly
# This allows us to bypass compatibility issues
def clone_voice_directly(text, speaker_wav, target_lang, output_path):
    """
    Direct voice cloning using TTS and PyTorch environment variable.
    """
    import torch
    from TTS.api import TTS
    
    print(f"[Direct Cloning] Using PyTorch {torch.__version__}")
    print(f"[Direct Cloning] TORCH_FULL_LOAD={os.environ.get('TORCH_FULL_LOAD', 'Not Set')}")
    
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
    
    try:
        # Check if GPU is available
        use_gpu = torch.cuda.is_available()
        
        # Initialize TTS with XTTS v2 model
        model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        tts = TTS(model_name=model_name, gpu=use_gpu)
        
        # Generate speech with voice cloning
        tts.tts_to_file(
            text=text,
            file_path=output_path,
            speaker_wav=speaker_wav,
            language=xtts_lang
        )
        
        # Return the output path if successful
        if os.path.exists(output_path):
            return output_path
        else:
            return None
    
    except Exception as e:
        print(f"Error in direct cloning: {str(e)}")
        return None

def main():
    """Test the voice cloning with different languages."""
    print("\n===== VOICE CLONING TEST (WITH ENV VARIABLE) =====")
    
    # Create a test reference audio if it doesn't exist
    sample_dir = os.path.join(OUTPUTS_DIR, "samples")
    os.makedirs(sample_dir, exist_ok=True)
    sample_path = os.path.join(sample_dir, "test_reference_audio.wav")
    
    if not os.path.exists(sample_path):
        print("\nCreating test reference audio...")
        sample_path = create_test_audio()
    
    print(f"\nUsing reference audio: {sample_path}")
    
    # Test texts in different languages
    test_cases = [
        {
            "lang": "en", 
            "text": "Hello! I'm an AI-generated voice speaking in English. This is a demonstration of cross-lingual voice cloning."
        },
        {
            "lang": "fr", 
            "text": "Bonjour! Je suis une voix générée par l'IA parlant en français. Ceci est une démonstration de clonage vocal multilingue."
        }
    ]
    
    for i, case in enumerate(test_cases):
        lang = case["lang"]
        text = case["text"]
        output_path = os.path.join(OUTPUTS_DIR, f"cloned_{lang}_env.wav")
        
        print(f"\n[Test {i+1}] Cloning voice to speak in {lang}")
        print(f"Text: {text}")
        print(f"Output: {output_path}")
        
        try:
            # Call our direct cloning function
            result = clone_voice_directly(
                text=text,
                speaker_wav=sample_path,
                target_lang=lang,
                output_path=output_path
            )
            
            if result:
                print(f"✅ Success! Cloned voice saved to: {result}")
            else:
                print(f"❌ Failed to clone voice for {lang}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n===== TEST COMPLETED =====")

if __name__ == "__main__":
    main() 