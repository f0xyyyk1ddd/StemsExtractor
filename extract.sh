#!/bin/bash
source venv/bin/activate

if [ -z "$1" ]; then
    echo "Usage: ./extract.sh <path_to_audio_file> [2|4|5]"
    echo "Example: ./extract.sh song.mp3 4"
    exit 1
fi

INPUT_FILE="$1"
STEMS="${2:-2}"

python cli.py "$INPUT_FILE" --stems "$STEMS"
