"""
Video Merger module for AI Dubbing project.
This module handles merging the original video with the newly generated dubbed audio.
"""

import os
import time
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from config.settings import TEMP_VIDEO_PATH, TEMP_DUBBED_AUDIO_PATH, OUTPUT_VIDEO_PATH
from utils.logger import setup_logger

logger = setup_logger(__name__)

def merge_video_audio_ffmpeg(video_path=TEMP_VIDEO_PATH, audio_path=TEMP_DUBBED_AUDIO_PATH, 
                          output_path=OUTPUT_VIDEO_PATH):
    """
    Merge video and audio using ffmpeg (precise, efficient).
    
    Args:
        video_path (str): Path to the input video file
        audio_path (str): Path to the input audio file
        output_path (str): Path to save the merged video
    
    Returns:
        str: Path to the merged video file, or None if merging failed
    """
    logger.info(f"Merging video and audio using ffmpeg: {video_path} + {audio_path}")
    
    # Check if input files exist
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return None
    if not os.path.exists(audio_path):
        logger.error(f"Audio file not found: {audio_path}")
        return None
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Prepare ffmpeg command
        # -y: Overwrite output without asking
        # -i: Input files
        # -map: Choose streams from input files
        # -c:v copy: Copy video stream without re-encoding
        # -shortest: End when the shortest input stream ends
        cmd = [
            "ffmpeg",
            "-y",
            "-i", video_path,
            "-i", audio_path,
            "-map", "0:v:0",  # First video stream from first input
            "-map", "1:a:0",  # First audio stream from second input
            "-c:v", "copy",   # Copy video codec
            "-c:a", "aac",    # Use AAC for audio
            "-b:a", "192k",   # Audio bitrate
            "-shortest",      # End when shortest input ends
            output_path
        ]
        
        # Execute ffmpeg command
        start_time = time.time()
        logger.debug(f"Running command: {' '.join(cmd)}")
        
        # Run the process
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        # Wait for process to complete
        stdout, stderr = process.communicate()
        
        # Check if process was successful
        if process.returncode != 0:
            logger.error(f"Error merging video and audio: {stderr.decode()}")
            return None
            
        merge_time = time.time() - start_time
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert to MB
        
        logger.info(f"Video and audio merged successfully to {output_path}")
        logger.info(f"Merge time: {merge_time:.2f} seconds, Size: {file_size:.2f} MB")
        
        return output_path
    
    except FileNotFoundError:
        logger.error("ffmpeg not found. Please install ffmpeg and ensure it's in your PATH.")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during video/audio merging: {str(e)}")
        return None

def merge_video_audio_moviepy(video_path=TEMP_VIDEO_PATH, audio_path=TEMP_DUBBED_AUDIO_PATH, 
                           output_path=OUTPUT_VIDEO_PATH):
    """
    Merge video and audio using moviepy (more flexible but slower).
    
    Args:
        video_path (str): Path to the input video file
        audio_path (str): Path to the input audio file
        output_path (str): Path to save the merged video
    
    Returns:
        str: Path to the merged video file, or None if merging failed
    """
    logger.info(f"Merging video and audio using moviepy: {video_path} + {audio_path}")
    
    # Check if input files exist
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return None
    if not os.path.exists(audio_path):
        logger.error(f"Audio file not found: {audio_path}")
        return None
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Load the video and audio clips
        start_time = time.time()
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        
        # Use the new audio for the video
        # If audio is longer than video, trim it to match video duration
        if audio_clip.duration > video_clip.duration:
            logger.info(f"Audio ({audio_clip.duration:.2f}s) longer than video ({video_clip.duration:.2f}s), trimming audio")
            audio_clip = audio_clip.subclip(0, video_clip.duration)
        
        # Set the audio of the video clip
        video_with_dubbed_audio = video_clip.set_audio(audio_clip)
        
        # Write the result to a file
        video_with_dubbed_audio.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )
        
        # Close the clips to release resources
        video_clip.close()
        audio_clip.close()
        video_with_dubbed_audio.close()
        
        merge_time = time.time() - start_time
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert to MB
        
        logger.info(f"Video and audio merged successfully to {output_path}")
        logger.info(f"Merge time: {merge_time:.2f} seconds, Size: {file_size:.2f} MB")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error merging video and audio with moviepy: {str(e)}")
        return None

def merge_video_audio(video_path=TEMP_VIDEO_PATH, audio_path=TEMP_DUBBED_AUDIO_PATH, 
                   output_path=OUTPUT_VIDEO_PATH, use_ffmpeg=True):
    """
    Merge video and audio using the specified method.
    
    Args:
        video_path (str): Path to the input video file
        audio_path (str): Path to the input audio file
        output_path (str): Path to save the merged video
        use_ffmpeg (bool): Whether to use ffmpeg (True) or moviepy (False)
    
    Returns:
        str: Path to the merged video file, or None if merging failed
    """
    if use_ffmpeg:
        try:
            # Try ffmpeg first (faster)
            return merge_video_audio_ffmpeg(video_path, audio_path, output_path)
        except Exception as e:
            logger.warning(f"ffmpeg merging failed: {str(e)}. Falling back to moviepy.")
            # Fall back to moviepy if ffmpeg fails
            return merge_video_audio_moviepy(video_path, audio_path, output_path)
    else:
        # Use moviepy directly
        return merge_video_audio_moviepy(video_path, audio_path, output_path)


# Example usage
if __name__ == "__main__":
    # Test with sample files (assuming they exist)
    if os.path.exists(TEMP_VIDEO_PATH) and os.path.exists(TEMP_DUBBED_AUDIO_PATH):
        merge_video_audio()
    else:
        print(f"Test files not found: {TEMP_VIDEO_PATH} or {TEMP_DUBBED_AUDIO_PATH}") 