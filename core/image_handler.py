import base64
import io
from PIL import Image

def encode_image (path: str)-> str:
    """
    Open an image, resize it to max 1024px,
    covert to JPEG, return as base64 string.
    """
    with Image.open(path) as img:
        # Convert to RGB (Handeles PNG transparency)
        img = img.convert("RGB")
        # Resize so it's not too large for API
        img.thumbnail((1024,2024))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        img_bytes = buffer.getvalue()
        
        return base64.b64encode(img_bytes).decode("utf-8")