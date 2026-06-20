import streamlit as st
from dotenv import load_dotenv
import tempfile
import os

# Load environment variables from .env locally
load_dotenv()

# Support Streamlit Cloud secrets too
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key

from core.image_handler import encode_image
from core.video_handler import extract_frame
from core.caption_genrator import generate_caption

# Page config
st.set_page_config(page_title="Caption Gen")
st.title("Instagram Caption Generator")

# Debug: Check API Key
api_key_found = bool(api_key)
st.write("Gemini Key Found:", api_key_found)

if not api_key_found:
    st.error("❌ GEMINI_API_KEY not found. Check Streamlit Secrets.")
    st.stop()

# Upload file
file = st.file_uploader(
    "Upload Photo or Video",
    type=["jpg", "jpeg", "png", "mp4", "mov"]
)

# Tone selection
tone = st.selectbox(
    "Choose Caption Tone",
    [
        "Aesthetic",
        "Funny",
        "Motivational",
        "Chill",
        "Professional",
        "Celebratory"
    ]
)

# Caption count
count = st.slider(
    "How many captions?",
    min_value=1,
    max_value=5,
    value=3
)

# Generate captions
if file and st.button("Generate Captions"):

    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(file.name)[1]
        ) as tmp:

            tmp.write(file.read())
            tmp.flush()
            tmp_path = tmp.name

        with st.spinner("AI is reading your media..."):

            ext = file.name.split(".")[-1].lower()

            if ext in ["mp4", "mov"]:
                st.write("📹 Processing video...")
                b64 = extract_frame(tmp_path)
            else:
                st.write("🖼️ Processing image...")
                b64 = encode_image(tmp_path)

            st.write("✅ Media processed successfully")

            result = generate_caption(
                b64,
                tone,
                count,
                api_key=api_key
            )

            st.success("Done! Here are your captions:")
            st.markdown(result)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.exception(e)

    finally:
        try:
            if 'tmp_path' in locals():
                os.unlink(tmp_path)
        except Exception:
            pass

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align:center;font-size:12px;color:#888;'>Made by DK_InnovAI</p>",
    unsafe_allow_html=True
)