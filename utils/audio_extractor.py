"""
Audio extraction module for AI Dubbing project.
This module handles extracting audio from video files using ffmpeg.
"""

import os
import subprocess
import time
from config.settings import TEMP_VIDEO_PATH, TEMP_AUDIO_PATH
from utils.logger import setup_logger

logger = setup_logger(__name__)

def extract_audio(video_path=TEMP_VIDEO_PATH, audio_path=TEMP_AUDIO_PATH, 
                 sample_rate=16000, channels=1):
    """
    Extract audio from a video file using ffmpeg.
    
    Args:
        video_path (str): Path to the input video file
        audio_path (str): Path to save the extracted audio
        sample_rate (int): Sampling rate for the extracted audio (default: 16kHz for STT)
        channels (int): Number of audio channels (1=mono, 2=stereo)
    
    Returns:
        str: Path to the extracted audio file, or None if extraction failed
    """
    logger.info(f"Extracting audio from video: {video_path}")
    
    # Check if video file exists
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return None
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    
    try:
        # Prepare ffmpeg command
        # -y: Overwrite output file without asking
        # -i: Input file
        # -vn: Disable video
        # -acodec: Audio codec (pcm_s16le = 16-bit PCM)
        # -ar: Audio sampling rate
        # -ac: Audio channels
        cmd = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", str(sample_rate),
            "-ac", str(channels),
            audio_path
        ]
        
        # Execute ffmpeg command
        start_time = time.time()
        logger.debug(f"Running command: {' '.join(cmd)}")
        
        # Run the process with output piped
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        # Wait for process to complete
        stdout, stderr = process.communicate()
        
        # Check if process was successful
        if process.returncode != 0:
            logger.error(f"Error extracting audio: {stderr.decode()}")
            return None
        
        extraction_time = time.time() - start_time
        file_size = os.path.getsize(audio_path) / (1024 * 1024)  # Convert to MB
        
        logger.info(f"Audio extracted successfully to {audio_path}")
        logger.info(f"Extraction time: {extraction_time:.2f} seconds, Size: {file_size:.2f} MB")
        logger.info(f"Audio settings: {sample_rate}Hz, {channels} channel(s)")
        
        return audio_path
        
    except FileNotFoundError:
        logger.error("ffmpeg not found. Please install ffmpeg and ensure it's in your PATH.")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during audio extraction: {str(e)}")
        return None


# Example usage
if __name__ == "__main__":
    # Test with a sample video file (assuming it exists)
    if os.path.exists(TEMP_VIDEO_PATH):
        extract_audio()
    else:
        print(f"Test video not found at {TEMP_VIDEO_PATH}") 