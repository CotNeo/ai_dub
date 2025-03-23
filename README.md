# AI Dubbing Project

A Python-based application that uses artificial intelligence technology to automatically dub YouTube videos into different languages.

## 🌟 Features

- Download YouTube videos directly from URL  
- Extract audio and transcribe speech to text  
- Translate text into the target language  
- Generate natural-sounding speech in the target language  
- Merge video with newly generated audio  
- Multiple TTS engine options (Bark, Coqui, Google TTS)  
- Voice cloning feature (dub using a reference voice)  
- Comprehensive logging system  

## 🔊 Voice Cloning

AI Dubbing offers the ability to dub in different languages using your own voice or any reference voice:

```bash
python main.py "https://www.youtube.com/watch?v=YOUTUBE_ID" \
  --source en \
  --target tr \
  --tts voice_clone \
  --reference-audio "path_to_your_reference_audio.wav"
```

### Overview

The Voice Cloning feature allows you to clone a voice from a reference audio sample and use it to generate speech in multiple languages. This creates a more personalized and consistent dubbing experience.

### How It Works

The voice cloning system uses two approaches:

1. **Primary Method (XTTS)**: When possible, the system uses the XTTS v2 model from the Coqui TTS library for high-quality voice cloning. This model can generate speech in multiple languages while preserving the characteristics of the reference voice.

2. **Fallback Method (gTTS)**: If the XTTS model cannot be loaded (due to incompatibility with PyTorch 2.6+ or other issues), the system automatically falls back to Google Text-to-Speech (gTTS) to generate speech in the target language.

### Record Your Own Voice

This tool also supports recording your own voice as a reference sample:

```bash
python main.py "https://www.youtube.com/watch?v=YOUTUBE_ID" \
  --source en \
  --target tr \
  --tts voice_clone \
  --record \
  --record-duration 10
```

This will prompt you to speak for 10 seconds to generate a reference sample, which will then be used for voice cloning.

### Voice Cloning Test

You can test the voice cloning feature directly using the provided test script:

```bash
python test_voice_cloner.py
```

This will generate sample audio files in multiple languages using the voice cloning feature.

### Supported Languages

The voice cloning feature supports the following languages:

- English (en)  
- French (fr)  
- Turkish (tr)  
- Spanish (es)  
- Italian (it)  
- German (de)  
- Portuguese (pt)  
- Polish (pl)  
- Russian (ru)  
- Dutch (nl)  
- Czech (cs)  
- Arabic (ar)  
- Chinese (zh)  
- Japanese (ja)  
- Korean (ko)  
- Hungarian (hu)  

### Troubleshooting

#### PyTorch 2.6+ Compatibility Issues

If you're using PyTorch 2.6 or newer, you may encounter compatibility issues with the XTTS model due to the `weights_only` parameter in `torch.load()`. The system is designed to handle this automatically and will fall back to gTTS, but if you want to use XTTS directly, try the following:

1. Set environment variable:
   ```bash
   export TORCH_FULL_LOAD=1
   ```

2. Add safe globals for PyTorch 2.6+:
   ```python
   from TTS.tts.configs.xtts_config import XttsConfig
   from TTS.tts.models.xtts import XttsAudioConfig
   import torch
   torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig])
   ```

#### Low Voice Cloning Quality

For the best voice cloning results:

1. Use a high-quality reference audio sample  
2. Ensure the reference audio is clear with minimal background noise  
3. Reference audio should be at least 3 seconds long  
4. Record in a quiet environment with good acoustic conditions  
5. Use a good quality microphone  

### Output Files

When using voice cloning, the system generates the following files:

- `outputs/dubbed_audio.wav`: The audio generated with the cloned voice  
- `outputs/dubbed_video.mp4`: Final video dubbed with the cloned voice  
- `outputs/samples/test_reference_audio.wav`: The reference audio sample (if recorded)  

## 🛠️ Technologies Used

- **Video Processing**: `pytube`, `ffmpeg`, `moviepy`  
- **Speech Recognition**: OpenAI Whisper (open-source)  
- **Translation**: Google Translate (unofficial), OpenAI GPT-3.5  
- **Text-to-Speech (TTS)**: Bark, Coqui TTS, Google TTS, XTTS (voice cloning)  
- **Logging**: Python's built-in logging module  

## 📋 Requirements

- Python 3.10 or higher  
- ffmpeg installed on your system  
- Required Python packages (see `requirements.txt`)  
- For voice cloning:  
  - TTS library (`pip install TTS`)  
  - gTTS library (`pip install gtts`)  
  - Reference audio file (.wav format, at least 3 seconds long)  

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/CotNeo/ai_dub.git
   cd ai_dub
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install ffmpeg:
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

5. Set API keys (optional):
   ```bash
   cp config/api_keys.py.example config/api_keys.py
   ```
   Edit the created `config/api_keys.py` file to add your own API keys.

   Alternatively, set API keys as environment variables:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   ```

6. (Optional) If using OpenAI services, configure your API keys in `config/settings.py`

## 🚀 Usage

### Basic Usage

Run the application with a YouTube URL:

```bash
python main.py https://www.youtube.com/watch?v=example_id
```

### Advanced Options

Specify source and target languages:

```bash
python main.py https://www.youtube.com/watch?v=example_id --source en --target tr
```

Available parameters:
- `--source` or `-s`: Source language code (default: en)  
- `--target` or `-t`: Target language code (default: tr)  
- `--tts`: TTS engine option (default: gtts, other options: bark, coqui, voice_clone)  
- `--reference-audio`: Reference audio file for voice cloning (used with voice_clone)  
- `--record`: Record reference audio (used with voice_clone)  
- `--record-duration`: Duration of recording in seconds (default: 10)  

## 🧹 Project Structure

```
ai_dub/
├── main.py                       # Main application entry point
├── config/
│   └── settings.py               # Configuration settings
├── utils/
│   ├── logger.py                 # Logging utility
│   ├── downloader.py             # YouTube video downloader
│   ├── audio_extractor.py        # Audio extractor
│   ├── transcriber.py            # Speech-to-text
│   ├── translator.py             # Text translation
│   ├── tts.py                    # Text-to-speech
│   ├── voice_cloner.py           # Voice cloning module
│   └── video_merger.py           # Merge video and audio
├── outputs/                      # Output and temporary files
├── logs/                         # Log files
├── requirements.txt              # Project dependencies
└── README.md                     # Project documentation
```

## ⚙️ Customization

You can customize the application by editing the `config/settings.py` file:

- Change default languages  
- Select different TTS engines  
- Configure model parameters  
- Set output file paths  

## 🤝 Contributing

Contributions are welcome! Feel free to submit a Pull Request.

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

## 🙏 Thanks

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition  
- [Bark](https://github.com/suno-ai/bark) and [Coqui TTS](https://github.com/coqui-ai/TTS) for text-to-speech capabilities  
- [pytube](https://github.com/pytube/pytube) for YouTube downloading functionality  
- [XTTS](https://coqui.ai/blog/tts/xtts-v2-improving-zero-shot-cross-lingual-text-to-speech) for voice cloning  
- [gTTS](https://github.com/pndurette/gTTS) as a fallback TTS option  

---

## 📞 Support

If you have any questions or encounter issues, please open an issue in this repository.

## 🧑‍💻 Developer

This project is developed by [CotNeo](https://github.com/CotNeo).



# AI Dublaj Projesi

Yapay zeka teknolojisini kullanarak YouTube videolarını farklı dillere otomatik olarak dublaj yapmanızı sağlayan Python tabanlı bir uygulama.

## 🌟 Özellikler

- YouTube videolarını URL'den doğrudan indirme
- Ses çıkarma ve konuşmayı metne dönüştürme
- Metni hedef dile çevirme
- Hedef dilde doğal sesli konuşma oluşturma
- Videoyu yeni oluşturulan sesle birleştirme
- Birden fazla TTS motor seçeneği (Bark, Coqui, Google TTS)
- Ses klonlama özelliği (referans ses ile dublaj)
- Kapsamlı günlük (log) sistemi

## 🔊 Ses Klonlama

AI Dublaj, kendi sesinizi veya herhangi bir referans sesi kullanarak, farklı dillerde dublaj yapabilme özelliği sunar:

```bash
python main.py "https://www.youtube.com/watch?v=YOUTUBE_ID" \
  --source en \
  --target tr \
  --tts voice_clone \
  --reference-audio "referans_sesinizin_yolu.wav"
```

### Genel Bakış

Ses Klonlama özelliği, bir referans ses örneğinden sesi klonlamanıza ve bu sesi birden fazla dilde konuşma oluşturmak için kullanmanıza olanak tanır. Bu, daha kişiselleştirilmiş ve tutarlı bir dublaj deneyimi yaratır.

### Nasıl Çalışır

Ses klonlama sistemi iki yaklaşım kullanır:

1. **Birincil Yöntem (XTTS)**: Mümkün olduğunda, sistem yüksek kaliteli ses klonlama için Coqui TTS kütüphanesinin XTTS v2 modelini kullanır. Bu model, referans sesin karakteristik özelliklerini korurken birden fazla dilde konuşma oluşturabilir.

2. **Yedek Yöntem (gTTS)**: XTTS modeli yüklenemezse (PyTorch 2.6+ ile uyumluluk sorunları veya başka nedenlerden dolayı), sistem otomatik olarak hedef dilde konuşma oluşturmak için Google Text-to-Speech (gTTS) kullanımına geçer.

### Kendi Sesinizi Kaydedin

Bu araç, referans örnek olarak kendi sesinizi kaydetmeyi de destekler:

```bash
python main.py "https://www.youtube.com/watch?v=YOUTUBE_ID" \
  --source en \
  --target tr \
  --tts voice_clone \
  --record \
  --record-duration 10
```

Bu, bir referans ses örneği oluşturmak için 10 saniye boyunca konuşmanızı isteyecek ve ardından bu örnek ses klonlama için kullanılacaktır.

### Ses Klonlama Testi

Ses klonlama özelliğini doğrudan sağlanan test betiği kullanarak test edebilirsiniz:

```bash
python test_voice_cloner.py
```

Bu, ses klonlama özelliğini kullanarak birden fazla dilde örnek ses dosyaları oluşturacaktır.

### Desteklenen Diller

Ses klonlama özelliği aşağıdaki dilleri destekler:

- İngilizce (en)
- Fransızca (fr)
- Türkçe (tr)
- İspanyolca (es)
- İtalyanca (it)
- Almanca (de)
- Portekizce (pt)
- Lehçe (pl)
- Rusça (ru)
- Hollandaca (nl)
- Çekçe (cs)
- Arapça (ar)
- Çince (zh)
- Japonca (ja)
- Korece (ko)
- Macarca (hu)

### Sorun Giderme

#### PyTorch 2.6+ Uyumluluk Sorunları

PyTorch 2.6 veya daha yeni bir sürüm kullanıyorsanız, `torch.load()` fonksiyonundaki `weights_only` parametresi nedeniyle XTTS modeliyle uyumluluk sorunları yaşayabilirsiniz. Sistem bunu otomatik olarak ele almak için tasarlanmıştır ve gTTS'ye geri döner, ancak XTTS'i doğrudan kullanmak istiyorsanız şunları deneyebilirsiniz:

1. Ortam değişkeni ayarlama:
   ```bash
   export TORCH_FULL_LOAD=1
   ```

2. PyTorch 2.6+ için güvenli globalleri ekleme:
   ```python
   from TTS.tts.configs.xtts_config import XttsConfig
   from TTS.tts.models.xtts import XttsAudioConfig
   import torch
   torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig])
   ```

#### Düşük Ses Klonlama Kalitesi

En iyi ses klonlama sonuçları için:

1. Yüksek kaliteli bir referans ses örneği kullanın
2. Referans sesin net olduğundan ve minimum arka plan gürültüsü içerdiğinden emin olun
3. Referans ses en az 3 saniye uzunluğunda olmalıdır
4. İyi akustik özelliklere sahip sessiz bir ortamda kaydedin
5. İyi kalitede bir mikrofon kullanın

### Çıktı Dosyaları

Ses klonlama kullanıldığında, sistem aşağıdaki dosyaları oluşturur:

- `outputs/dubbed_audio.wav`: Klonlanmış sesle oluşturulan ses
- `outputs/dubbed_video.mp4`: Klonlanmış sesle orjinal videonun üzerine dublaj yapılmış son video
- `outputs/samples/test_reference_audio.wav`: Referans ses örneği (kayıt yoluyla oluşturulmuşsa)

## 🛠️ Kullanılan Teknolojiler

- **Video İşleme**: `pytube`, `ffmpeg`, `moviepy`
- **Konuşma Tanıma**: OpenAI Whisper (açık kaynak)
- **Çeviri**: Google Translate (gayri resmi), OpenAI GPT-3.5
- **Metinden Sese Dönüştürme**: Bark, Coqui TTS, Google TTS, XTTS (ses klonlama)
- **Günlük Tutma**: Python'un dahili logging modülü

## 📋 Gereksinimler

- Python 3.10 veya daha yüksek
- Sisteminizde kurulu ffmpeg
- Gerekli Python paketleri (bkz. `requirements.txt`)
- Ses klonlama için:
  - TTS kütüphanesi (`pip install TTS`)
  - gTTS kütüphanesi (`pip install gtts`)
  - Referans ses dosyası (.wav formatında, en az 3 saniye uzunluğunda)

## 🔧 Kurulum

1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/CotNeo/ai_dub.git
   cd ai_dub
   ```

2. Sanal ortam oluşturun (önerilir):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Gerekli bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

4. ffmpeg'i yükleyin:
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **Windows**: [ffmpeg.org](https://ffmpeg.org/download.html) adresinden indirin ve PATH'e ekleyin

5. API anahtarlarını ayarlayın (isteğe bağlı):
   ```bash
   cp config/api_keys.py.example config/api_keys.py
   ```
   Oluşturulan `config/api_keys.py` dosyasını düzenleyerek kendi API anahtarlarınızı ekleyin.

   Alternatif olarak, API anahtarlarını çevre değişkenleri olarak ayarlayabilirsiniz:
   ```bash
   export OPENAI_API_KEY="sizin_openai_api_anahtarınız"
   ```

6. (İsteğe bağlı) OpenAI hizmetlerini kullanıyorsanız `config/settings.py` içinde API anahtarlarını ayarlayın

## 🚀 Kullanım

### Temel Kullanım

Uygulamayı bir YouTube URL'si ile çalıştırın:

```bash
python main.py https://www.youtube.com/watch?v=ornek_id
```

### Gelişmiş Seçenekler

Kaynak ve hedef dilleri belirtin:

```bash
python main.py https://www.youtube.com/watch?v=ornek_id --source en --target tr
```

Kullanılabilir parametreler:
- `--source` veya `-s`: Kaynak dil kodu (varsayılan: en)
- `--target` veya `-t`: Hedef dil kodu (varsayılan: tr)
- `--tts`: TTS motoru seçeneği (varsayılan: gtts, diğer seçenekler: bark, coqui, voice_clone)
- `--reference-audio`: Ses klonlama için referans ses dosyası (voice_clone ile kullanılır)
- `--record`: Referans ses kaydı yapmak için (voice_clone ile kullanılır)
- `--record-duration`: Kayıt süresi saniye cinsinden (varsayılan: 10)

## 🧩 Proje Yapısı

```
ai_dub/
├── main.py                       # Ana uygulama giriş noktası
├── config/
│   └── settings.py               # Yapılandırma ayarları
├── utils/
│   ├── logger.py                 # Günlük (log) yardımcı programı
│   ├── downloader.py             # YouTube video indirici
│   ├── audio_extractor.py        # Videodan ses çıkarma
│   ├── transcriber.py            # Konuşmadan metne dönüştürme
│   ├── translator.py             # Metin çevirisi
│   ├── tts.py                    # Metinden sese dönüştürme
│   ├── voice_cloner.py           # Ses klonlama modülü
│   └── video_merger.py           # Video ve ses birleştirme
├── outputs/                      # Çıktı ve geçici dosyalar
├── logs/                         # Günlük dosyaları
├── requirements.txt              # Proje bağımlılıkları
└── README.md                     # Proje dokümantasyonu
```

## ⚙️ Özelleştirme

`config/settings.py` dosyasını düzenleyerek uygulamayı özelleştirebilirsiniz:

- Varsayılan dilleri değiştirme
- Farklı TTS motoru seçme
- Model parametrelerini yapılandırma
- Çıktı dosya konumlarını ayarlama

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen bir Pull Request göndermekten çekinmeyin.

## 📜 Lisans

Bu proje açık kaynaklıdır ve [MIT Lisansı](LICENSE) altında kullanılabilir.

## 🙏 Teşekkürler

- Konuşma tanıma kabiliyeti için [OpenAI Whisper](https://github.com/openai/whisper)
- Metinden sese dönüştürme kabiliyetleri için [Bark](https://github.com/suno-ai/bark) ve [Coqui TTS](https://github.com/coqui-ai/TTS)
- YouTube indirme işlevselliği için [pytube](https://github.com/pytube/pytube)
- Ses klonlama için [XTTS](https://coqui.ai/blog/tts/xtts-v2-improving-zero-shot-cross-lingual-text-to-speech)
- Yedek metin-konuşma oluşturma için [gTTS](https://github.com/pndurette/gTTS)

---

## 📞 Destek

Herhangi bir sorunuz varsa veya sorunlarla karşılaşırsanız, lütfen bu depoda bir sorun (issue) açın.

## 🧑‍💻 Geliştirici

Bu proje [CotNeo](https://github.com/CotNeo) tarafından geliştirilmiştir. 

