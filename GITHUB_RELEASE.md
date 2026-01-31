# 🚀 Публикация релиза на GitHub

## Шаг 1: Создание репозитория на GitHub

1. Откройте [github.com/new](https://github.com/new)
2. Заполните:
   - **Repository name:** `StemsExtractor`
   - **Description:** `🎵 AI-Powered Music Source Separation - Extract vocals, drums, bass from any song`
   - **Visibility:** Public (или Private)
   - ❌ Не ставьте галочки на README, .gitignore, LICENSE (они уже есть)
3. Нажмите **Create repository**

---

## Шаг 2: Подключение локального репозитория
it re
После создания репозитория выполните команды:

```bash
# Замените YOUR_USERNAME на ваше имя пользователя GitHub
gmote add origin https://github.com/YOUR_USERNAME/StemsExtractor.git

# Переименуем ветку в main (если нужно)
git branch -M main

# Отправляем код
git push -u origin main

# Отправляем тег релиза
git push origin v1.0.0
```

---

## Шаг 3: Создание Release на GitHub

### Через веб-интерфейс:

1. Перейдите на страницу репозитория
2. Нажмите **Releases** (справа)
3. Нажмите **Create a new release**
4. Заполните:
   - **Choose a tag:** `v1.0.0`
   - **Release title:** `🎉 Stems Extractor Pro v1.0.0`
   - **Description:** (см. ниже)
5. Прикрепите файлы (если есть .app или .exe)
6. Нажмите **Publish release**

### Описание релиза (Release Notes):

```markdown
# 🎉 Stems Extractor Pro v1.0.0

**Initial Release - AI-Powered Music Source Separation**

## ✨ Features

- 🎤 **2-Stem Separation** - Vocals + Instrumental
- 🥁 **4-Stem Separation** - Vocals + Drums + Bass + Other
- 🎹 **5-Stem Separation** - Vocals + Drums + Bass + Piano + Other
- 🖥️ **Modern Dark GUI** - Beautiful PyQt5 interface
- 💻 **CLI Support** - Command-line for automation
- 🌐 **Web Interface** - Browser-based FastAPI server

## 📦 Supported Formats

**Input:** MP3, WAV, FLAC, M4A, AIFF, OGG
**Output:** WAV (44100Hz, 16-bit, high quality)

## 💻 System Requirements

- Python 3.8 - 3.11
- 8GB RAM (16GB recommended)
- macOS 10.13+ / Windows 10+ / Linux

## 🚀 Quick Start

\`\`\`bash
git clone https://github.com/YOUR_USERNAME/StemsExtractor.git
cd StemsExtractor
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install PyQt5 static-ffmpeg
python gui.py
\`\`\`

## 📖 Documentation

- [Full Documentation (Russian)](DOCUMENTATION_RU.md)
- [Quick Start (Russian)](QUICK_START_RU.md)

## 📄 License

This project is licensed under the GNU General Public License v3 (GPLv3).

---

**FOR DJ'S BY DJ'S** 🎧

Made with ❤️ by SCVDL & f0xyyy133
```

---

## Шаг 4: Прикрепление бинарников (опционально)

Если вы собрали .app или .exe, прикрепите их к релизу:

1. Заархивируйте `dist/StemsExtractor.app` → `StemsExtractor-v1.0.0-macOS.zip`
2. Заархивируйте `dist/StemsExtractor/` (Windows) → `StemsExtractor-v1.0.0-Windows.zip`
3. Перетащите файлы в раздел "Attach binaries" при создании релиза

---

## 🎯 Готово!

После выполнения этих шагов ваш проект будет доступен по адресу:
```
https://github.com/YOUR_USERNAME/StemsExtractor
```

---

## Полезные команды Git

```bash
# Проверить статус
git status

# Посмотреть логи
git log --oneline -5

# Посмотреть теги
git tag

# Посмотреть remote
git remote -v
```
