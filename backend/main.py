import os
import shutil
import asyncio
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import static_ffmpeg

# Ensure ffmpeg is in path
static_ffmpeg.add_paths()

app = FastAPI()

# --- Config ---
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"
FRONTEND_DIR = BASE_DIR / "frontend"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Spleeter Logic ---
from spleeter.separator import Separator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_spleeter(file_path: str, stems: int):
    """
    Runs Spleeter separation using the Python API.
    """
    try:
        # Check for ffmpeg
        if not shutil.which("ffmpeg"):
            logger.error("FFmpeg not found")
            return False, "FFmpeg not found. Please install FFmpeg."

        logger.info(f"Starting separation for {file_path} with {stems} stems")
        
        # Initialize Separator
        # Note: This might download models to ~/.cache/spleeter on first run
        separator = Separator(f"spleeter:{stems}stems")
        
        # Run separation
        # Using synchronous call since we are already in a thread/executor
        separator.separate_to_file(file_path, str(OUTPUT_DIR))
        
        logger.info("Separation complete")
        return True, "Success"
        
    except Exception as e:
        logger.error(f"Spleeter error: {e}", exc_info=True)
        return False, str(e)

# --- API ---
@app.get("/")
async def read_index():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/api/separate")
async def separate_audio(
    file: UploadFile = File(...),
    stems: int = Form(...)
):
    if stems not in [2, 4, 5]:
        return JSONResponse({"status": "error", "message": "Invalid stems count"}, status_code=400)

    # Save file
    safe_filename = file.filename.replace(" ", "_").replace("(", "").replace(")", "")
    file_path = UPLOAD_DIR / safe_filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Run Spleeter
    # Note: Spleeter takes time, we run it in a thread/process to not block async loop
    # Ideally use background tasks, but we want to await result for this simple UI
    
    loop = asyncio.get_event_loop()
    success, message = await loop.run_in_executor(None, run_spleeter, str(file_path), stems)
    
    if not success:
         return JSONResponse({"status": "error", "message": message})

    # Find results
    # Spleeter creates a folder with the name of the file (minus extension)
    track_name = Path(safe_filename).stem
    track_output_dir = OUTPUT_DIR / track_name
    
    if not track_output_dir.exists():
        return JSONResponse({"status": "error", "message": "Output directory not found. Separation might have failed silently."})
    
    # Map results
    results = {}
    for audio_file in track_output_dir.glob("*.wav"):
        # URL mapping: /output/{track_name}/{stem_file}
        results[audio_file.stem] = f"/output/{track_name}/{audio_file.name}"
        
    return {"status": "success", "result": results}

# --- Static Files ---
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")
# Mount frontend content
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    print("Starting server at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
