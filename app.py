import streamlit as st
from dotenv import load_dotenv
from core.image_handler import encode_image
from core.video_handler import extract_frame
from core.caption_genrator import generate_caption
import tempfile,os

load_dotenv()

st.set_page_config(page_title="Caption Gen")
st.title("Instgram Caption Generator")

file=st.file_uploader(
    "Upload Photo or Video",
    type=["jpg","png","jpeg","mp4","mov"]
    )

tone=st.selectbox("Choose Caption Tone",[
    "Aesthetic","Funny","Motivational",
    "Chill","Professional","Celebratory"
])

count=st.slider("How many captions?",1,5,3)

if file and st.button("Generate Captions"):
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(file.name)[1]
        ) as tmp:
        tmp.write(file.read())
        tmp.flush()
        tmp_path=tmp.name
    
    # File is now closed, safe to read
    with st.spinner("AI is reading your media..."):
        ext = file.name.split(".")[-1].lower()
        if ext in ["mp4","mov"]:
            b64=extract_frame(tmp_path)
        else:
            b64 = encode_image(tmp_path)
        
        result=generate_caption(b64,tone,count)
        st.success("Done! here are your captions:")
        st.markdown(result)
    
    try:
        os.unlink(tmp_path)
    except Exception as e:
        print(f"Could not delete temp file: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #888;'>Made by DK_InnovAI</p>", unsafe_allow_html=True)