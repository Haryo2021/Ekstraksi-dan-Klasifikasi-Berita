import streamlit as st
from src.scraper import scrape_berita
from src.predictor import predict_points
from src.summarizer import summarize_to_points
from src.ui import render_header
from src.preprocessing import preprocess_text

def switch_to_manual():
    st.session_state.mode = "Teks manual"
    if "input_link" in st.session_state:
        st.session_state.input_link = ""

def reset_values():
    st.session_state.reset_values += 1 
    st.session_state.input_link = ""

if 'reset_values' not in st.session_state:
    st.session_state.reset_values = 0

def run_link_mode(model, vectorizer):
    with st.expander("Penjelasan"):
        st.write("Untuk mode link ini, anda hanya menempelkan link berita, aplikasi memproses berita tersebut dan memberikan poin penting.")
    input_key = f"input_link_{st.session_state.reset_values}"
    input_link = st.text_input("Masukkan Link atau URL berita", key=input_key)  
    if st.button("Ambil poin penting pada berita", use_container_width=True):
        if not input_link.strip():
            st.warning("Harap masukan link...")
            return
            
        with st.spinner("Mengambil konten berita..."):
            raw_text = scrape_berita(input_link)
            if not raw_text:
                st.error("Mohon maaf untuk saat ini, link belum bisa mengambil teks pada artikel berita ini, silahkan masukkan link yang lain atau gunakan mode manual")
                st.button("Pindah ke mode manual", on_click=switch_to_manual)
                return
            summary_points = summarize_to_points(raw_text, n_points=3)

            bg_color = "#F7F7F7"
            border_color = "#373838"
            title_color = "#000000"

            points_html = "".join([f"<li style='margin-bottom: 8px;'>{p}</li>" for p in summary_points])

            st.markdown(f"""
                <div style="
                    background-color: {bg_color}
                    width: 350px;
                    border-radius: 25px; 
                    border: 2px solid {border_color};
                    margin-top: 20px;
                    margin-bottom: 20px;
                ">
                    <h3 style='text-align: center; color: {title_color};'>
                        📌 Poin Penting pada Berita
                    </h3>
                    <hr style="border: 7px solid {border_color};">
                    <ul style="text-align: left; color: #000000; font-size: 15px;">
                        {points_html}
                    </ul>
                </div>
            """, unsafe_allow_html=True)
                    
            pred = predict_points(raw_text, model, vectorizer)
            st.markdown(
                f"""
                <div style="
                    background-color: #E8F5E9;
                    padding: 16px;
                    border-radius: 8px;
                    border-left: 6px solid #2E7D32;
                    color: #000000;
                    font-size: 16px;
                ">
                    <b>Kategori berita adalah</b> {pred.upper()}
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.expander("Isi berita asli"):
                st.write(raw_text[:10000])

            st.button ("Mengambil link yang lain", on_click=reset_values)

    
