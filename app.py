import streamlit as st
from src.model_loader import load_model
from mode.link import run_link_mode
from mode.manual import run_manual_mode
from src.ui import render_header
import nltk 
import os
from huggingface_hub import login

hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(token=hf_token)
    
@st.cache_resource
def setup_nltk():
    nltk_data_path = "/home/appuser/nltk_data"
    os.makedirs(nltk_data_path, exist_ok=True)
    nltk.data.path.append(nltk_data_path)

    nltk.download("punkt", download_dir=nltk_data_path)
    nltk.download("punkt_tab", download_dir=nltk_data_path)

setup_nltk()

if "reset_values" not in st.session_state:
    st.session_state.reset_values = 0

if "mode" not in st.session_state:
    st.session_state.mode = "Link berita"

st.set_page_config(page_title="Ekstraksi dan Klasifikasi Berita", layout="centered")

st.markdown(f"""<h1 style=
                "text-align: center;
                color: #000000;">
                Klasifikasi berita dan Ekstraksi poin penting pada berita Hukum, Politik, dan Teknologi.
                </h1>
                 """, unsafe_allow_html=True)
st.subheader("Aplikasi ini akan mengambil poin penting pada berita agar dapat memahami konteks pada berita yang ingin dibaca.")

render_header()

model, vectorizer = load_model()

if "mode" not in st.session_state:
    st.session_state.mode = "Link berita"

st.write("Pilih mode inputan: ")
col1, col2 = st.columns(2)

with col1:
    is_link = st.session_state.mode == "Link berita"
    if st.button("Mode link", use_container_width=True, type="primary" if is_link else "secondary"):
        st.session_state.mode = "Link berita"

with col2:
    is_manual = st.session_state.mode == "Teks manual"
    if st.button("Mode manual", use_container_width=True, type="primary" if is_manual else "secondary"):
        st.session_state.mode = "Teks manual"

if model and vectorizer:    
    if st.session_state.mode == "Link berita":
        run_link_mode(model, vectorizer)
    else:
        run_manual_mode(model, vectorizer)
else:
    st.error("Model tidak tersedia, pastikan file pkl model dan vectorizer ada.")
