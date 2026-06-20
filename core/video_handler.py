import cv2
import base64
import numpy as np

def extract_frame(path: str) -> str:
    """
    Open video, jump to the middle frame,
    encode as JPEG base64 for Claude API.
    """
    cap = cv2.VideoCapture(path)
    
    # Get total frame count
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Jump to the middle of the video
    middle = total_frames //2
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle)
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        raise ValueError("Could not read video frame")
    
    # Encode frame as JPEG
    _, buffer = cv2.imencode(
        ".jpg", frame,
        [cv2.IMWRITE_JPEG_QUALITY, 85]
    )
    
    return base64.b64encode(buffer).decode("utf-8")