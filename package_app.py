
import os
import shutil
import plistlib
from pathlib import Path

DIST_DIR = Path("dist")
APP_NAME = "StemsExtractor.app"
APP_DIR = DIST_DIR / APP_NAME
CONTENTS_DIR = APP_DIR / "Contents"
MACOS_DIR = CONTENTS_DIR / "MacOS"
RESOURCES_DIR = CONTENTS_DIR / "Resources"

# 1. Clean up
if APP_DIR.exists():
    shutil.rmtree(APP_DIR)

# 2. Create Structure
MACOS_DIR.mkdir(parents=True, exist_ok=True)
RESOURCES_DIR.mkdir(parents=True, exist_ok=True)

# 3. Move/Copy Build
# We expect dist/StemsExtractor to contain the build
SOURCE_BUILD = DIST_DIR / "StemsExtractor"

if not SOURCE_BUILD.exists():
    print(f"Error: {SOURCE_BUILD} does not exist.")
    exit(1)

# Move all content from dist/StemsExtractor to Contents/MacOS/
for item in SOURCE_BUILD.iterdir():
    # If using move, we need to be careful not to move inside itself if paths overlap, 
    # but here SOURCE_BUILD is dist/StemsExtractor and DEST is dist/StemsExtractor.app/Contents/MacOS
    shutil.move(str(item), str(MACOS_DIR))

# Remove the empty source dir
SOURCE_BUILD.rmdir()

# 4. Create Info.plist
info_plist = {
    'CFBundleName': 'Stems Extractor Pro',
    'CFBundleDisplayName': 'Stems Extractor',
    'CFBundleIdentifier': 'com.scvdl.stemsextractor',
    'CFBundleVersion': '1.0.0',
    'CFBundleShortVersionString': '1.0.0',
    'CFBundlePackageType': 'APPL',
    'CFBundleSignature': '????',
    'CFBundleExecutable': 'StemsExtractor',
    'CFBundleIconFile': 'icon.icns',
    'NSHighResolutionCapable': True,
    'LSMinimumSystemVersion': '10.13.0'
}

with open(CONTENTS_DIR / "Info.plist", "wb") as f:
    plistlib.dump(info_plist, f)

# 5. Icon
# Converting png to icns is tricky without iconutil, but we can try just copying png as icon.icns 
# (macOS sometimes handles it) or just icon.png if we change plist.
# Ideally we use sips or iconutil.
# We have logo.png in the root.
LOGO_PATH = Path("logo_clean.png")
if LOGO_PATH.exists():
    # Create an iconset folder
    iconset = Path("StemsExtractor.iconset")
    iconset.mkdir(exist_ok=True)
    
    # Resize to standard sizes
    import subprocess
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for s in sizes:
        subprocess.run(["sips", "-z", str(s), str(s), str(LOGO_PATH), "--out", str(iconset / f"icon_{s}x{s}.png")], capture_output=True)
        subprocess.run(["sips", "-z", str(s*2), str(s*2), str(LOGO_PATH), "--out", str(iconset / f"icon_{s}x{s}@2x.png")], capture_output=True)
        
    # Convert to icns
    subprocess.run(["iconutil", "-c", "icns", str(iconset), "-o", str(RESOURCES_DIR / "icon.icns")], capture_output=True)
    
    # Cleanup
    shutil.rmtree(iconset)
else:
    print("Warning: logo.png not found")

# 6. Fix for Python Shared Library (Frameworks)
# PyInstaller bundle mode expects python dylib in Frameworks, but onedir puts it in _internal.
# We symlink Frameworks -> MacOS/_internal to satisfy both the loader and the python path.
FRAMEWORKS_PATH = CONTENTS_DIR / "Frameworks"
INTERNAL_PATH = Path("MacOS/_internal") # Relative to Frameworks parent (Contents)

# Note: We need to create the symlink relative to the Contents directory
# Symlink: dist/StemsExtractor.app/Contents/Frameworks -> MacOS/_internal
if not FRAMEWORKS_PATH.exists():
    os.symlink("MacOS/_internal", FRAMEWORKS_PATH)

print(f"Successfully packaged {APP_DIR}")
