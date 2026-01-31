import argparse
import sys
import shutil
from pathlib import Path
import logging
import static_ffmpeg

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("StemsExtractor")

def main():
    parser = argparse.ArgumentParser(description="Extract stems from audio files.")
    parser.add_argument("input_file", help="Path to the audio file")
    parser.add_argument("--stems", type=int, choices=[2, 4, 5], default=2, help="Number of stems (2, 4, 5)")
    parser.add_argument("--output", default="output", help="Output directory")
    
    args = parser.parse_args()
    
    # 1. Setup FFmpeg
    logger.info("Checking FFmpeg...")
    static_ffmpeg.add_paths()
    
    if not shutil.which("ffmpeg"):
         logger.error("❌ FFmpeg not found even after static setup. Please install it manually.")
         sys.exit(1)

    input_path = Path(args.input_file)
    if not input_path.exists():
        logger.error(f"❌ File not found: {args.input_file}")
        sys.exit(1)
        
    # 2. Import Spleeter (lazy load to show progress)
    logger.info("Loading AI models (Spleeter)...")
    try:
        # Spleeter implies tensorflow, which can be noisy
        import os
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TF logging
        from spleeter.separator import Separator
    except ImportError as e:
        logger.error(f"❌ Failed to load Spleeter: {e}")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"❌ Error loading libraries: {e}")
        sys.exit(1)
    
    # 3. Process
    logger.info(f"🎵 Separating '{input_path.name}' into {args.stems} stems...")
    logger.info("This process might take a few minutes (especially first run to download models)...")
    
    try:
        separator = Separator(f"spleeter:{args.stems}stems")
        separator.separate_to_file(str(input_path), args.output)
        logger.info(f"✅ Success! Output saved to: {Path(args.output).resolve()}/{input_path.stem}")
    except Exception as e:
        logger.error(f"❌ Error during separation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
