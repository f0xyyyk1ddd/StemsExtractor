# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-31

### Added
- 🎉 Initial release
- Modern dark-themed GUI application (PyQt5)
- Command-line interface (CLI) for automation
- Web interface with FastAPI backend
- Support for 2, 4, and 5 stem separation modes
- Support for MP3, WAV, FLAC, M4A, AIFF, OGG input formats
- High-quality WAV output (44100Hz, 16-bit)
- macOS .app packaging support
- Windows .exe packaging support
- Russian documentation
- Auto-bundled FFmpeg via static-ffmpeg

### Technical
- Spleeter integration for AI-powered source separation
- TensorFlow backend
- PyInstaller build configuration
- Cross-platform compatibility

---

## Roadmap

### Planned for v1.1.0
- [ ] Demucs model support (higher quality)
- [ ] Drag & drop file support
- [ ] Batch processing in GUI
- [ ] Progress percentage display
- [ ] Output format selection (MP3, FLAC)
- [ ] Model training guide

### Planned for v1.2.0
- [ ] GPU acceleration support
- [ ] Custom model import
- [ ] Audio preview before export
- [ ] Queue management
