import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_caption(
    b64_image:str,
    tone:str,
    count:int = 3
    )-> str:
    """
    Send base64 image to Google Gemini 2.5 Flash.
    Returns Instagram captions with hashtags.
    """
    
    # ===== OLD CODE (COMMENTED OUT) =====
    # import anthropic
    # client = anthropic.Anthropic(
    #     api_key=os.getenv("GEMINI_API_KEY")
    #     )
    # prompt=f"""Look at this image carefully.
    #     Genrate exactly {count} Instgram caption in a
    #     **{tone}**tone.
    #     
    #     Formt your response like this:
    #     **Caption 1:**
    #     [caption text here]
    #     #hashtag1  #hashtag2  #hashtag3..
    #     
    #     **Caption 2:**
    #     [caption text here]
    #     #hashtag1  #hashtag2  #hashtag3..
    #     
    #     Rules:
    #     -Each caption should feel natural for Instgaram
    #     -Include 5-10 relevant hashtags per caption
    #     -Match the {tone} tone perfectly
    #     -Keep captions between 1-3 sentences"""
    #
    # message=client.messages.create(
    #      model="claude-sonnet-4-2050514",
    #      max_tokens=1000,
    #      messages=[
    #         {
    #             "role":"user",
    #             "content":[
    #                 {
    #                     "type":"image",
    #                     "source":{
    #                         "type":"base64",
    #                         "media_type":"image/jpeg",
    #                         "data":b64_image,
    #                          
    #                     },
    #                 },
    #                 {
    #                     "type":"text",
    #                     "text":prompt
    #                 }
    #             ],
    #         }
    #     ],
    #  )
    # return message.content[0].text
    # ===== END OLD CODE =====
    
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
    