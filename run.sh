#!/bin/bash
export PATH=$PWD:$PATH
echo "Checking dependencies..."
if ! command -v ffmpeg &> /dev/null
then
    echo "⚠️  FFmpeg could not be found. separations will fail until it is installed."
    echo "Mac: brew install ffmpeg"
    # Proceeding anyway so UI can be viewed
fi

echo "Starting Stems Extractor..."
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:.
export PATH=$PWD:$PATH
python backend/main.py
