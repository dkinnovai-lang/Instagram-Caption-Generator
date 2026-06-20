import os

ALLOWED_IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_VIDEO_TYPES = {".mp4", ".mov", ".avi", ".mkv"}
MAX_FILE_SIZE_MB = 50

def is_image(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_IMAGE_TYPES

def is_video(filename: str) -> bool:
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_VIDEO_TYPES

def is_valid_size(path: str) -> bool:
    size_md = os.path.getsize(path) /(1024 * 1024)
    return size_md <= MAX_FILE_SIZE_MB

def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

def cleanup_file(path: str) -> None:
    """Safely delete a temp file."""
    
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass  #Fail Silently