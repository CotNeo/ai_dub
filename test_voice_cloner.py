"""
Test script for the Voice Cloning module.
This script demonstrates how to use the voice_cloner_fallback module.
"""

import os
import sys
from pathlib import Path
import torch

# Add the project root to the path so we can import our modules
sys.path.append(str(Path(__file__).parent))

# Register safe globals for PyTorch 2.6+ compatibility
try:
    from TTS.tts.configs.xtts_config import XttsConfig
    torch.serialization.add_safe_globals([XttsConfig])
except (ImportError, AttributeError):
    # Handle cases where TTS is not installed or PyTorch version doesn't support add_safe_globals
    pass

# Import our fallback voice cloner module
from utils.voice_cloner_fallback import clone_voice_and_speak
from utils.create_test_audio import create_test_audio
from config.settings import OUTPUTS_DIR

def main():
    """Test the voice cloning module with different languages."""
    print("\n===== VOICE CLONING TEST (FALLBACK) =====")
    
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
            "lang": "tr", 
            "text": "Merhaba! Ben Türkçe konuşan yapay zeka tarafından oluşturulmuş bir sesim. Bu, diller arası ses klonlamanın bir gösterimi."
        },
        {
            "lang": "fr", 
            "text": "Bonjour! Je suis une voix générée par l'IA parlant en français. Ceci est une démonstration de clonage vocal multilingue."
        }
    ]
    
    for i, case in enumerate(test_cases):
        lang = case["lang"]
        text = case["text"]
        output_path = os.path.join(OUTPUTS_DIR, f"cloned_{lang}_fallback.mp3")
        
        print(f"\n[Test {i+1}] Generating voice in {lang}")
        print(f"Text: {text}")
        print(f"Output: {output_path}")
        
        try:
            # Use our fallback voice cloner
            result = clone_voice_and_speak(
                text=text,
                speaker_wav_path=sample_path,
                target_lang=lang,
                output_path=output_path
            )
            
            if result:
                print(f"✅ Success! Voice saved to: {result}")
            else:
                print(f"❌ Failed to generate voice for {lang}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n===== TEST COMPLETED =====")

if __name__ == "__main__":
    main() 