"""
Test Audio Creator Script.
Creates a sample reference audio file for voice cloning testing.
"""

import os
import sys

# Add parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import OUTPUTS_DIR
from gtts import gTTS

def create_test_audio():
    """Create a test reference audio file using gTTS."""
    print("Creating test reference audio file...")
    
    # Create samples directory if it doesn't exist
    samples_dir = os.path.join(OUTPUTS_DIR, "samples")
    os.makedirs(samples_dir, exist_ok=True)
    
    # Path for the test audio file
    test_audio_path = os.path.join(samples_dir, "test_reference_audio.wav")
    
    # Create a short audio clip using gTTS
    test_text = "This is a test reference audio for voice cloning. Hello world!"
    tts = gTTS(text=test_text, lang="en", slow=False)
    
    # Save as mp3 first (gtts can only output mp3)
    temp_mp3_path = os.path.join(samples_dir, "temp.mp3")
    tts.save(temp_mp3_path)
    
    # Convert mp3 to wav using ffmpeg if available, otherwise keep the mp3
    try:
        import subprocess
        subprocess.run([
            "ffmpeg", "-y", "-i", temp_mp3_path, "-acodec", "pcm_s16le", 
            "-ar", "16000", "-ac", "1", test_audio_path
        ], check=True)
        os.remove(temp_mp3_path)
        print(f"Created test reference audio file: {test_audio_path}")
    except Exception as e:
        # If ffmpeg fails or isn't available, just use the mp3
        test_audio_path = temp_mp3_path
        print(f"Could not convert to WAV. Created MP3 instead: {test_audio_path}")
        print(f"Error: {str(e)}")
    
    return test_audio_path

if __name__ == "__main__":
    audio_path = create_test_audio()
    print(f"Test audio created at: {audio_path}") 