<p align="center">
  <img src="logo.png" alt="Stems Extractor Pro" width="128">
</p>

<h1 align="center">🎵 Stems Extractor Pro</h1>

<p align="center">
  <strong>AI-Powered Music Source Separation</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/platform-macOS%20|%20Windows%20|%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
</p>

---

## 🎯 About

**Stems Extractor Pro** is a professional application for separating music tracks into individual instrument stems using artificial intelligence and neural networks.

Built with [Spleeter](https://github.com/deezer/spleeter) by Deezer Research, it provides high-quality audio source separation with an elegant, modern interface.

> **"FOR DJ'S BY DJ'S"** 🎧

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎤 **2-Stem Separation** | Vocals + Instrumental |
| 🥁 **4-Stem Separation** | Vocals + Drums + Bass + Other |
| 🎹 **5-Stem Separation** | Vocals + Drums + Bass + Piano + Other |
| 🖥️ **Modern GUI** | Dark-themed PyQt5 interface |
| 💻 **CLI Support** | Command-line for automation |
| 🌐 **Web Interface** | Browser-based FastAPI server |
| 📁 **Batch Processing** | Process multiple files |

---

## 📦 Installation

### Prerequisites

- **Python 3.8 - 3.11**
- **FFmpeg** (automatically handled by `static-ffmpeg`)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/StemsExtractor.git
cd StemsExtractor

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install PyQt5 static-ffmpeg
```

### Manual FFmpeg Installation (if needed)

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

---

## 🚀 Usage

### GUI Application

```bash
python gui.py
```

1. Click **"Select Audio File"**
2. Choose separation mode (2, 4, or 5 stems)
3. Click **"START PROCESSING"**
4. Results saved to `output/` folder

### Command Line

```bash
# Basic usage
python cli.py "song.mp3"

# With options
python cli.py "song.mp3" --stems 4 --output "my_output"
```

### Web Interface

```bash
python backend/main.py
# Open http://127.0.0.1:8000
```

---

## 📁 Supported Formats

| Input | Output |
|-------|--------|
| MP3, WAV, FLAC, M4A, AIFF, OGG | WAV (44100Hz, 16-bit) |

---

## 📖 Documentation

- 🇷🇺 [Полная документация (Russian)](DOCUMENTATION_RU.md)
- 🇷🇺 [Быстрый старт (Russian)](QUICK_START_RU.md)

---

## 🗂️ Project Structure

```
StemsExtractor/
├── gui.py                 # Main GUI application
├── cli.py                 # Command-line interface
├── requirements.txt       # Python dependencies
├── logo.png              # Application logo
│
├── backend/
│   └── main.py           # FastAPI web server
│
├── frontend/
│   ├── index.html        # Web interface
│   ├── style.css         # Styles
│   └── script.js         # JavaScript
│
├── uploads/              # Uploaded files (web)
└── output/               # Separation results
```

---

## 🏗️ Building

### macOS (.app)

```bash
pip install pyinstaller
pyinstaller GuiApp.spec
python package_app.py
```

### Windows (.exe)

```cmd
build_windows.bat
```

---

## 🙏 Acknowledgments

- [Spleeter](https://github.com/deezer/spleeter) - Deezer Research
- [TensorFlow](https://www.tensorflow.org/) - Machine Learning Platform
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI Framework
- [FastAPI](https://fastapi.tiangolo.com/) - Web Framework

---

## 👨‍💻 Authors

- **SCVDL** - Lead Developer
- **f0xyyy133** - Co-Developer

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>Made with ❤️ for the DJ community</strong>
</p>
