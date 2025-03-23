"""
Audio Recorder module for AI Dubbing project.
This module handles recording audio from the microphone for voice cloning.
"""

import os
import time
import pyaudio
import wave
import tempfile
from tqdm import tqdm
from config.settings import OUTPUTS_DIR
from utils.logger import setup_logger

logger = setup_logger(__name__)

def record_audio(output_path=None, sample_rate=16000, channels=1, duration=10):
    """
    Record audio from the microphone.
    
    Args:
        output_path (str): Path to save the recorded audio file
        sample_rate (int): Sample rate of the recording
        channels (int): Number of audio channels
        duration (int): Duration of the recording in seconds
        
    Returns:
        str: Path to the recorded audio file, or None if recording failed
    """
    try:
        # If output path not provided, create one
        if not output_path:
            os.makedirs(os.path.join(OUTPUTS_DIR, "samples"), exist_ok=True)
            timestamp = int(time.time())
            output_path = os.path.join(OUTPUTS_DIR, "samples", f"reference_audio_{timestamp}.wav")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Set audio parameters
        chunk = 1024  # Record in chunks of 1024 samples
        audio_format = pyaudio.paInt16  # 16-bit resolution
        
        logger.info(f"Starting audio recording: {output_path}")
        print(f"\n🎙️ Ses kaydı başlatılıyor... ({duration} saniye)")
        print("Lütfen konuşmaya başlayın...")
        
        # Initialize PyAudio
        audio = pyaudio.PyAudio()
        
        # Open stream
        stream = audio.open(
            format=audio_format,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk
        )
        
        frames = []
        
        # Create a progress bar
        with tqdm(total=duration, desc="Kayıt", bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [saniye]") as pbar:
            # Record for the specified duration
            for i in range(0, int(sample_rate / chunk * duration)):
                data = stream.read(chunk)
                frames.append(data)
                
                # Update progress bar every second
                if i % int(sample_rate / chunk) == 0:
                    pbar.update(1)
        
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Save the audio file
        with wave.open(output_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(audio_format))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
        
        logger.info(f"Audio recording saved to {output_path}")
        print(f"\n✅ Kayıt tamamlandı: {output_path}")
        
        # Get file size
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert to MB
        logger.info(f"Recording size: {file_size:.2f} MB")
        print(f"📊 Dosya boyutu: {file_size:.2f} MB")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error recording audio: {str(e)}")
        print(f"\n❌ HATA: Ses kaydedilemedi: {str(e)}")
        return None

def test_audio_device():
    """
    Test if an audio input device is available.
    
    Returns:
        bool: True if at least one input device is available, False otherwise
    """
    try:
        audio = pyaudio.PyAudio()
        device_count = audio.get_device_count()
        
        # Check if there's at least one input device
        has_input = False
        for i in range(device_count):
            device_info = audio.get_device_info_by_index(i)
            if device_info.get('maxInputChannels') > 0:
                has_input = True
                break
                
        audio.terminate()
        return has_input
        
    except Exception as e:
        logger.error(f"Error testing audio device: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    if test_audio_device():
        print("Audio input device found. Starting recording...")
        record_audio(duration=5)
    else:
        print("No audio input device found.") 