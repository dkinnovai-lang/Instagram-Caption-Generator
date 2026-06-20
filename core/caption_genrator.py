import google.generativeai as genai
import os


def generate_caption(
    b64_image:str,
    tone:str,
    count:int = 3,
    api_key:str | None = None
    )-> str:
    """
    Send base64 image to Google Gemini 2.5 Flash.
    Returns Instagram captions with hashtags.
    """

    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")

    genai.configure(api_key=api_key)
    """
    Send base64 image to Google Gemini 2.5 Flash.
    Returns Instagram captions with hashtags.
    """
    
    # NEW CODE: Using Google Gemini 2.5 Flash
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""Look at this image carefully.
Generate exactly {count} Instagram caption in a
**{tone}** tone.

Format your response like this:
**Caption 1:**
[caption text here]
#hashtag1 #hashtag2 #hashtag3..

**Caption 2:**
[caption text here]
#hashtag1 #hashtag2 #hashtag3..

Rules:
- Each caption should feel natural for Instagram
- Include 5-10 relevant hashtags per caption
- Match the {tone} tone perfectly
- Keep captions between 1-3 sentences"""
    
    # Convert base64 to image bytes
    import base64
    image_bytes = base64.b64decode(b64_image)
    
    # Generate content with image
    response = model.generate_content([
        {
            "mime_type": "image/jpeg",
            "data": image_bytes,
        },
        prompt
    ])
    
    return response.text
    