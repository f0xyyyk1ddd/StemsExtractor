#!/bin/bash
rm -rf StemsExtractor.iconset
mkdir -p StemsExtractor.iconset

INPUT_FILE="logo_clean.png"

sips -z 16 16     $INPUT_FILE --setProperty format png --out StemsExtractor.iconset/icon_16x16.png
sips -z 32 32     $INPUT_FILE --setProperty format png --out StemsExtractor.iconset/icon_16x16@2x.png
sips -z 32 32     $INPUT_FILE --setProperty format png --out StemsExtractor.iconset/icon_32x32.png
sips -z 64 64     $INPUT_FILE --setProperty format png --out StemsExtractor.iconset/icon_32x32@2x.png
sips -z 128 128   $INPUT_FILE --setProperty format png --out StemsExtractor.iconset/icon_128x128.png
sips -z 256 256   $INPUT_FILE --setProperty format png --out StemsExtractor.iconset/icon_128x128@2x.png
sips -z 256 256   $INPUT_FILE --setProperty format png --out StemsExtractor.iconset/icon_256x256.png
sips -z 512 512   $INPUT_FILE --setProperty format png --out StemsExtractor.iconset/icon_256x256@2x.png
sips -z 512 512   $INPUT_FILE --setProperty format png --out StemsExtractor.iconset/icon_512x512.png
sips -z 1024 1024 $INPUT_FILE --setProperty format png --out StemsExtractor.iconset/icon_512x512@2x.png

iconutil -c icns StemsExtractor.iconset -o icon.icns
