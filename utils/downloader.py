"""
YouTube video downloader module for AI Dubbing project.
This module handles downloading videos from YouTube using pytube.
"""

import os
import time
import requests
import subprocess
from pytube import YouTube
from pytube.exceptions import PytubeError
from tqdm import tqdm
from config.settings import TEMP_VIDEO_PATH
from utils.logger import setup_logger

logger = setup_logger(__name__)

def download_video_with_yt_dlp(url, output_path=TEMP_VIDEO_PATH, resolution="720"):
    """
    Alternative method to download a YouTube video using yt-dlp (if installed).
    This is more robust than pytube for some videos.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Path to save the downloaded video
        resolution (str): Video resolution to download
        
    Returns:
        str: Path to the downloaded video file, or None if download failed
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        logger.info(f"Attempting to download with yt-dlp: {url}")
        print(f"⚠️ Pytube failed, trying alternative download method...")
        
        # Construct yt-dlp command
        # -f: Format to download (here we're getting the best video with audio up to specified resolution)
        # -o: Output filename
        # --no-playlist: Don't download the playlist even if the URL points to one
        cmd = [
            "yt-dlp",
            "-f", f"best[height<={resolution}]",
            "-o", output_path,
            "--no-playlist",
            url
        ]
        
        # Execute the command
        start_time = time.time()
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Display progress
        while process.poll() is None:
            line = process.stdout.readline().strip()
            if line and '[download]' in line and '%' in line:
                print(f"\r{line}", end='', flush=True)
                
        # Get the return code
        return_code = process.wait()
        
        # Process the result
        if return_code != 0:
            stderr = process.stderr.read()
            logger.error(f"yt-dlp error: {stderr}")
            return None
            
        download_time = time.time() - start_time
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        
        logger.info(f"Video downloaded successfully using yt-dlp to {output_path}")
        logger.info(f"Download time: {download_time:.2f} seconds, Size: {file_size:.2f} MB")
        
        return output_path
        
    except FileNotFoundError:
        logger.error("yt-dlp is not installed. Install it with 'pip install yt-dlp'")
        return None
    except Exception as e:
        logger.error(f"Error using yt-dlp: {str(e)}")
        return None

def download_youtube_video(url, output_path=TEMP_VIDEO_PATH, resolution="720p"):
    """
    Download a YouTube video at the specified URL.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Path to save the downloaded video
        resolution (str): Video resolution to download
    
    Returns:
        str: Path to the downloaded video file, or None if download failed
    """
    logger.info(f"Downloading YouTube video: {url}")
    
    try:
        # Create progress bar
        progress_bar = None
        
        def on_progress(stream, chunk, bytes_remaining):
            nonlocal progress_bar
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            
            if progress_bar is None:
                progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, 
                                  desc="Downloading", leave=True)
            
            progress_bar.update(chunk)
        
        # Create YouTube object with progress callback
        yt = YouTube(url, on_progress_callback=on_progress)
        logger.info(f"Video title: {yt.title}")
        
        # Get the appropriate stream
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4', 
                                        resolution=resolution).first()
        
        # If requested resolution isn't available, get the highest one
        if not video_stream:
            logger.warning(f"Resolution {resolution} not available. Getting highest resolution.")
            video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Download the video
        start_time = time.time()
        video_stream.download(output_path=os.path.dirname(output_path), 
                            filename=os.path.basename(output_path))
        
        if progress_bar:
            progress_bar.close()
            
        download_time = time.time() - start_time
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert to MB
        
        logger.info(f"Video downloaded successfully to {output_path}")
        logger.info(f"Download time: {download_time:.2f} seconds, Size: {file_size:.2f} MB")
        
        return output_path
        
    except PytubeError as e:
        logger.error(f"Error downloading YouTube video with pytube: {str(e)}")
        logger.info("Trying alternative download method...")
        # Try using yt-dlp as a fallback
        return download_video_with_yt_dlp(url, output_path, resolution.replace("p", ""))
    except Exception as e:
        logger.error(f"Unexpected error during download: {str(e)}")
        # Try using yt-dlp as a fallback
        return download_video_with_yt_dlp(url, output_path, resolution.replace("p", ""))


# Example usage
if __name__ == "__main__":
    # Test with a royalty-free YouTube video
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    download_youtube_video(test_url) 