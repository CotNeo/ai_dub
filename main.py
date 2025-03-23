"""
AI Dubbing Project - Main Script
This script orchestrates the entire dubbing process, from downloading a YouTube video
to generating the final dubbed video.

Usage:
    python main.py [youtube_url] [source_language] [target_language]
"""

import os
import sys
import time
import argparse
from datetime import timedelta
from config.settings import (
    SOURCE_LANGUAGE, TARGET_LANGUAGE, OUTPUT_VIDEO_PATH,
    TEMP_VIDEO_PATH, TEMP_AUDIO_PATH, TEMP_TRANSCRIPT_PATH,
    TEMP_TRANSLATED_PATH, TEMP_DUBBED_AUDIO_PATH,
    WHISPER_MODEL, TRANSLATION_ENGINE, TTS_ENGINE,
    REFERENCE_AUDIO_PATH
)
from utils.logger import setup_logger
from utils.downloader import download_youtube_video
from utils.audio_extractor import extract_audio
from utils.transcriber import transcribe_audio
from utils.translator import translate_file
from utils.tts import text_to_speech
from utils.video_merger import merge_video_audio
from utils.voice_cloner_fallback import clone_voice_and_speak
try:
    from utils.audio_recorder import record_audio, test_audio_device
    HAS_AUDIO_RECORDER = True
except ImportError:
    HAS_AUDIO_RECORDER = False

# Set up logger
logger = setup_logger(__name__)

def format_time(seconds):
    """Format seconds into a readable time string."""
    return str(timedelta(seconds=int(seconds)))

def print_stage_header(stage, title):
    """Print a formatted stage header to the console."""
    print("\n" + "=" * 80)
    print(f"[AŞAMA {stage}/6] {title}")
    print("-" * 80)

def print_stage_completion(stage, title, time_taken):
    """Print a formatted stage completion message."""
    print("-" * 80)
    print(f"✅ AŞAMA {stage}/6 TAMAMLANDI: {title}")
    print(f"⏱️ Geçen süre: {format_time(time_taken)}")
    print("=" * 80)

def get_file_size_mb(file_path):
    """Get file size in MB."""
    if os.path.exists(file_path):
        return os.path.getsize(file_path) / (1024 * 1024)
    return 0

def process_video(youtube_url, source_lang=SOURCE_LANGUAGE, target_lang=TARGET_LANGUAGE, 
                tts_engine=TTS_ENGINE, reference_audio=None):
    """
    Process a YouTube video through the entire dubbing pipeline.
    
    Args:
        youtube_url (str): URL of the YouTube video to process
        source_lang (str): Source language code
        target_lang (str): Target language code
        tts_engine (str): TTS engine to use
        reference_audio (str): Path to reference audio file for voice cloning
        
    Returns:
        str: Path to the output dubbed video, or None if processing failed
    """
    try:
        total_start_time = time.time()
        
        # Print welcome message
        print("\n" + "=" * 80)
        print(f"🎬 AI DUBLAJ PROJESİ BAŞLATILIYOR")
        print(f"🔗 Video URL: {youtube_url}")
        print(f"🈯 Kaynak dil: {source_lang} → Hedef dil: {target_lang}")
        print(f"⚙️ Yapılandırma: Whisper {WHISPER_MODEL}, Çeviri: {TRANSLATION_ENGINE}, TTS: {tts_engine}")
        if tts_engine == "voice_clone" and reference_audio:
            print(f"🎤 Ses Klonlama: Referans ses dosyası: {reference_audio}")
        print("=" * 80)
        
        logger.info("=" * 50)
        logger.info(f"Starting AI dubbing process for: {youtube_url}")
        logger.info(f"Source language: {source_lang}, Target language: {target_lang}")
        logger.info("=" * 50)
        
        # Step 1: Download the YouTube video
        print_stage_header(1, "YOUTUBE VİDEOSU İNDİRİLİYOR")
        print(f"URL: {youtube_url}")
        print(f"Hedef: {TEMP_VIDEO_PATH}")
        
        step_start_time = time.time()
        video_path = download_youtube_video(youtube_url, TEMP_VIDEO_PATH)
        step_time = time.time() - step_start_time
        
        if not video_path:
            print("❌ HATA: Video indirilemedi!")
            logger.error("Failed to download video. Exiting.")
            return None
            
        video_size = get_file_size_mb(video_path)
        print(f"📊 Video boyutu: {video_size:.2f} MB")
        print_stage_completion(1, "YOUTUBE VİDEOSU İNDİRİLDİ", step_time)
        
        # Step 2: Extract audio from the video
        print_stage_header(2, "VİDEODAN SES ÇIKARILIYOR")
        print(f"Kaynak: {video_path}")
        print(f"Hedef: {TEMP_AUDIO_PATH}")
        
        step_start_time = time.time()
        audio_path = extract_audio(video_path, TEMP_AUDIO_PATH)
        step_time = time.time() - step_start_time
        
        if not audio_path:
            print("❌ HATA: Ses çıkarılamadı!")
            logger.error("Failed to extract audio. Exiting.")
            return None
            
        audio_size = get_file_size_mb(audio_path)
        print(f"📊 Ses dosya boyutu: {audio_size:.2f} MB")
        print_stage_completion(2, "SES ÇIKARMA TAMAMLANDI", step_time)
        
        # Step 3: Transcribe the audio to text
        print_stage_header(3, "SES METİNE ÇEVRİLİYOR")
        print(f"Kullanılan model: Whisper {WHISPER_MODEL}")
        print(f"Kaynak dil: {source_lang}")
        print(f"Kaynak: {audio_path}")
        print(f"Hedef: {TEMP_TRANSCRIPT_PATH}")
        
        step_start_time = time.time()
        transcript_path = transcribe_audio(audio_path, TEMP_TRANSCRIPT_PATH, language=source_lang)
        step_time = time.time() - step_start_time
        
        if not transcript_path:
            print("❌ HATA: Ses metine çevrilemedi!")
            logger.error("Failed to transcribe audio. Exiting.")
            return None
            
        # Get transcript length (character count)
        transcript_length = 0
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = f.read()
            transcript_length = len(transcript)
            
        print(f"📝 Transkript uzunluğu: {transcript_length} karakter")
        print(f"📊 İlk 100 karakter: {transcript[:100]}...")
        print_stage_completion(3, "TRANSKRIPT OLUŞTURULDU", step_time)
        
        # Step 4: Translate the transcription
        print_stage_header(4, "METİN ÇEVRİLİYOR")
        print(f"Çeviri motoru: {TRANSLATION_ENGINE}")
        print(f"Dil çifti: {source_lang} → {target_lang}")
        print(f"Kaynak: {transcript_path}")
        print(f"Hedef: {TEMP_TRANSLATED_PATH}")
        
        step_start_time = time.time()
        translated_path = translate_file(transcript_path, TEMP_TRANSLATED_PATH, 
                                      source_lang=source_lang, target_lang=target_lang)
        step_time = time.time() - step_start_time
        
        if not translated_path:
            print("❌ HATA: Metin çevrilemedi!")
            logger.error("Failed to translate text. Exiting.")
            return None
            
        # Get translation length
        translation_length = 0
        with open(translated_path, 'r', encoding='utf-8') as f:
            translation = f.read()
            translation_length = len(translation)
            
        print(f"📝 Çeviri uzunluğu: {translation_length} karakter")
        print(f"📊 İlk 100 karakter: {translation[:100]}...")
        print_stage_completion(4, "ÇEVİRİ TAMAMLANDI", step_time)
        
        # Step 5: Generate speech from translated text
        print_stage_header(5, "ÇEVİRİLEN METİN SESE DÖNÜŞTÜRÜLÜYOR")
        print(f"TTS motoru: {tts_engine}")
        if tts_engine == "voice_clone" and reference_audio:
            print(f"Referans ses: {reference_audio}")
        print(f"Dil: {target_lang}")
        print(f"Kaynak: {translated_path}")
        print(f"Hedef: {TEMP_DUBBED_AUDIO_PATH}")
        
        step_start_time = time.time()
        
        # Use direct voice cloning if engine is set to voice_clone
        if tts_engine == "voice_clone" and reference_audio:
            # Read the translated text
            with open(translated_path, 'r', encoding='utf-8') as f:
                translated_text = f.read()
                
            # Call our fallback voice cloner
            dubbed_audio_path = clone_voice_and_speak(
                text=translated_text,
                speaker_wav_path=reference_audio,
                target_lang=target_lang,
                output_path=TEMP_DUBBED_AUDIO_PATH
            )
        else:
            # Otherwise, use the regular text_to_speech function
            dubbed_audio_path = text_to_speech(
                translated_path, 
                TEMP_DUBBED_AUDIO_PATH, 
                language=target_lang,
                engine=tts_engine,
                reference_audio=reference_audio
            )
            
        step_time = time.time() - step_start_time
        
        if not dubbed_audio_path:
            print("❌ HATA: Metin sese dönüştürülemedi!")
            logger.error("Failed to generate speech. Exiting.")
            return None
            
        dubbed_audio_size = get_file_size_mb(dubbed_audio_path)
        print(f"📊 Oluşturulan ses dosyası boyutu: {dubbed_audio_size:.2f} MB")
        print_stage_completion(5, "SESLER OLUŞTURULDU", step_time)
        
        # Step 6: Merge the video with the new audio
        print_stage_header(6, "VİDEO YENİ SESLE BİRLEŞTİRİLİYOR")
        print(f"Video kaynağı: {video_path}")
        print(f"Ses kaynağı: {dubbed_audio_path}")
        print(f"Hedef: {OUTPUT_VIDEO_PATH}")
        
        step_start_time = time.time()
        output_path = merge_video_audio(video_path, dubbed_audio_path, OUTPUT_VIDEO_PATH)
        step_time = time.time() - step_start_time
        
        if not output_path:
            print("❌ HATA: Video ve ses birleştirilemedi!")
            logger.error("Failed to merge video and audio. Exiting.")
            return None
            
        output_size = get_file_size_mb(output_path)
        print(f"📊 Final video boyutu: {output_size:.2f} MB")
        print_stage_completion(6, "VİDEO BİRLEŞTİRME TAMAMLANDI", step_time)
        
        # Process completed successfully
        total_time = time.time() - total_start_time
        
        print("\n" + "=" * 80)
        print(f"🎉 AI DUBLAJ İŞLEMİ BAŞARIYLA TAMAMLANDI!")
        print(f"⏱️ Toplam işlem süresi: {format_time(total_time)} ({total_time:.2f} saniye)")
        print(f"💾 Çıktı video: {output_path}")
        print(f"📊 Final dosya boyutu: {output_size:.2f} MB")
        print("=" * 80)
        
        logger.info("=" * 50)
        logger.info(f"AI dubbing process completed successfully!")
        logger.info(f"Total processing time: {total_time:.2f} seconds")
        logger.info(f"Output video saved to: {output_path}")
        logger.info("=" * 50)
        
        return output_path
        
    except Exception as e:
        logger.error(f"Unexpected error during dubbing process: {str(e)}")
        print(f"\n❌ HATA: İşlem sırasında beklenmeyen bir hata oluştu: {str(e)}")
        return None

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="AI Dubbing Tool - Convert YouTube videos to another language")
    
    parser.add_argument("youtube_url", nargs="?", 
                      help="YouTube video URL to process")
    
    parser.add_argument("--source", "-s", dest="source_lang", default=SOURCE_LANGUAGE,
                      help=f"Source language code (default: {SOURCE_LANGUAGE})")
    
    parser.add_argument("--target", "-t", dest="target_lang", default="ask",
                      help=f"Target language code (default: will prompt for input)")
    
    parser.add_argument("--tts", dest="tts_engine", default=TTS_ENGINE,
                      choices=["gtts", "bark", "coqui", "voice_clone", "ask"],
                      help=f"TTS engine to use (default: {TTS_ENGINE})")
    
    parser.add_argument("--reference-audio", dest="reference_audio", 
                      help="Path to reference audio file for voice cloning")
                      
    parser.add_argument("--record", "-r", action="store_true",
                      help="Record reference audio for voice cloning")
                      
    parser.add_argument("--record-duration", dest="record_duration", type=int, default=10,
                      help="Duration of reference audio recording in seconds (default: 10)")
    
    return parser.parse_args()

def main():
    """Main entry point for the AI dubbing application."""
    args = parse_arguments()
    
    # If no URL provided, prompt the user
    youtube_url = args.youtube_url
    if not youtube_url:
        youtube_url = input("Enter YouTube URL to process: ")
    
    # If no target language provided or if user wants to be prompted, ask for it
    target_lang = args.target_lang
    if not target_lang or target_lang.lower() == "ask":
        print("\nAvailable target languages:")
        print("  tr: Turkish")
        print("  en: English")
        print("  fr: French")
        print("  es: Spanish")
        print("  de: German")
        print("  ru: Russian")
        print("  zh: Chinese")
        print("  ja: Japanese")
        print("  ko: Korean")
        print("  ar: Arabic")
        print("  (More languages may be available depending on the TTS engine)")
        
        target_lang = input("\nEnter target language code: ")
        while not target_lang.strip():
            target_lang = input("Target language cannot be empty. Enter target language code: ")
    
    # Allow user to select TTS engine if not specified or "ask" is used
    tts_engine = args.tts_engine
    if tts_engine.lower() == "ask":
        print("\nAvailable TTS (Text-to-Speech) engines:")
        print("  1. gtts: Google TTS (hızlı, kararlı)")
        print("  2. voice_clone: Ses Klonlama (yüksek kalite, referans ses gerektirir)")
        print("  3. bark: Bark AI (yüksek kalite, yavaş)")
        print("  4. coqui: Coqui TTS (orta kalite)")
        
        choice = input("\nTTS motorunu seçin (1-4): ")
        while not choice.strip() or choice not in ["1", "2", "3", "4"]:
            choice = input("Geçersiz seçim. TTS motorunu seçin (1-4): ")
        
        # Map choice to TTS engine
        tts_engines = {
            "1": "gtts",
            "2": "voice_clone",
            "3": "bark",
            "4": "coqui"
        }
        tts_engine = tts_engines[choice]
    
    # Handle reference audio for voice cloning
    reference_audio = args.reference_audio
    
    # If voice cloning is selected
    if tts_engine.lower() == "voice_clone":
        # If record flag is set, record reference audio
        if args.record:
            if not HAS_AUDIO_RECORDER:
                print("\n❌ HATA: Ses kayıt özelliği kullanılamıyor. PyAudio kütüphanesi eksik.")
                print("Lütfen 'pip install pyaudio' komutu ile yükleyin.")
                return 1
                
            # Check if audio device is available
            if not test_audio_device():
                print("\n❌ HATA: Ses kayıt cihazı bulunamadı.")
                print("Lütfen bir mikrofon bağlayın ve tekrar deneyin.")
                return 1
                
            # Record reference audio
            reference_audio = record_audio(duration=args.record_duration)
            if not reference_audio:
                print("\n❌ HATA: Ses kaydedilemedi.")
                return 1
                
        # If no reference audio is provided or recording failed, ask for path
        elif not reference_audio:
            print("\n🎤 Ses klonlama motoru seçildi.")
            reference_audio = input("Referans ses dosyasının yolunu girin (örn. /path/to/voice.wav): ")
            
            # Validate that the reference audio file exists
            while not reference_audio.strip() or not os.path.exists(reference_audio):
                if not reference_audio.strip():
                    reference_audio = input("Referans ses dosyası boş olamaz. Lütfen geçerli bir dosya yolu girin: ")
                else:
                    print(f"Dosya bulunamadı: {reference_audio}")
                    reference_audio = input("Lütfen geçerli bir referans ses dosyası yolu girin: ")
    
    # Process the video
    output_path = process_video(
        youtube_url, 
        args.source_lang, 
        target_lang, 
        tts_engine, 
        reference_audio
    )
    
    # Check if processing was successful
    if output_path and os.path.exists(output_path):
        print(f"\n✅ Başarılı! Dublajlı video kaydedildi: {output_path}")
        return 0
    else:
        print("\n❌ Dublajlı video oluşturulamadı. Detaylar için log dosyasını kontrol edin.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 