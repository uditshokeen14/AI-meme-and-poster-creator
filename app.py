import streamlit as st
import os
import requests
from PIL import Image
from io import BytesIO
from caption_generator import generate_captions
from poster_generator import create_poster

st.set_page_config(page_title="AI Meme & Poster Creator", layout="wide")

TEMPLATE_FOLDER = r"C:\Users\ayush\OneDrive\Desktop\AI_Meme_Poster_Creator\templates"

# ----------------------------
# REDDIT STYLE CSS
# ----------------------------
st.markdown("""
<style>
.stApp { background-color: #0f0f10; }
h1 { color: #ff4500; font-weight: 800; }
h2, h3, h4 { color: #d7dadc; }
.block-container { padding-top: 2rem; }

.stTextInput>div>div>input,
.stTextArea textarea,
.stSelectbox>div>div,
.stRadio>div {
    background-color: #1a1a1b !important;
    color: white !important;
    border-radius: 10px;
    border: 1px solid #343536;
}

.stButton>button {
    background-color: #ff4500;
    color: white;
    border-radius: 25px;
    border: none;
    font-weight: 600;
}

.stButton>button:hover {
    background-color: #e03d00;
}

section[data-testid="stSidebar"] {
    background-color: #1a1a1b;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎨 AI Meme & Poster Creator</h1>", unsafe_allow_html=True)
st.markdown("---")

# ----------------------------
# SESSION STATE INIT
# ----------------------------
if "captions" not in st.session_state:
    st.session_state.captions = []

if "selected_caption" not in st.session_state:
    st.session_state.selected_caption = None

if "manual_mode" not in st.session_state:
    st.session_state.manual_mode = False

if "last_event" not in st.session_state:
    st.session_state.last_event = None

if "internet_template_loaded" not in st.session_state:
    st.session_state.internet_template_loaded = False

# ----------------------------
# SIDEBAR SETTINGS
# ----------------------------
with st.sidebar:
    st.title("⚙ Customization")

    template_source = st.radio(
        "Template Source",
        ["Local Templates", "Random Internet Template"]
    )

    available_fonts = [
        f for f in os.listdir("fonts") if f.endswith(".ttf")
    ]

    selected_font = st.selectbox("Choose Font", available_fonts)
    font_size = st.slider("Font Size", 20, 80, 40)

# ----------------------------
# MAIN CONTENT
# ----------------------------
event_name = st.text_input("Enter Event Name")

col1, col2 = st.columns(2)

with col1:
    if st.button("✍ Write Your Own Caption"):
        st.session_state.manual_mode = True

with col2:
    if st.button("🔄 Refresh Suggestions"):
        if event_name:
            st.session_state.captions = generate_captions(event_name)
            st.session_state.selected_caption = None
            st.session_state.manual_mode = False

# ----------------------------
# Generate captions ONLY when event changes
# ----------------------------
if event_name:
    if st.session_state.last_event != event_name:
        st.session_state.captions = generate_captions(event_name)
        st.session_state.last_event = event_name
        st.session_state.selected_caption = None
        st.session_state.manual_mode = False

st.markdown("---")
st.markdown("### 🖼 Template Selection")

selected_template_path = None

# LOCAL TEMPLATE
if template_source == "Local Templates":
    templates = [
        f for f in os.listdir(TEMPLATE_FOLDER)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    selected_template = st.selectbox("Choose Template", templates)
    selected_template_path = os.path.join(TEMPLATE_FOLDER, selected_template)

# INTERNET TEMPLATE
else:
    if st.button("Get Random Internet Template"):
        try:
            image_url = "https://picsum.photos/800/1000"
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            image.save("random_template.png")
            st.session_state.internet_template_loaded = True
            st.toast("Random template loaded!")
        except:
            st.error("Failed to load template.")

    if st.session_state.internet_template_loaded:
        st.image("random_template.png", use_container_width=True)
        selected_template_path = "random_template.png"

st.markdown("---")
st.markdown("### ✍ Caption Section")

# Manual Mode
if st.session_state.manual_mode:
    manual_caption = st.text_area("Type your caption here")
    if manual_caption:
        st.session_state.selected_caption = manual_caption

# AI Suggestions
else:
    if st.session_state.captions:
        selected = st.radio(
            "AI Suggestions",
            st.session_state.captions,
            index=0 if st.session_state.selected_caption is None
            else st.session_state.captions.index(st.session_state.selected_caption)
            if st.session_state.selected_caption in st.session_state.captions
            else 0
        )
        st.session_state.selected_caption = selected

st.markdown("---")

# ----------------------------
# GENERATE POSTER
# ----------------------------
if st.button("🚀 Generate Poster"):

    if st.session_state.selected_caption and selected_template_path:

        output_path = create_poster(
            selected_template_path,
            st.session_state.selected_caption,
            font_name=selected_font,
            font_size=font_size
        )

        st.markdown("### 🖼 Generated Poster")
        st.image(output_path, use_container_width=True)

        with open(output_path, "rb") as file:
            st.download_button(
                label="⬇ Download Poster",
                data=file,
                file_name="poster.png",
                mime="image/png"
            )
    else:
        st.warning("Please select template and caption first.")