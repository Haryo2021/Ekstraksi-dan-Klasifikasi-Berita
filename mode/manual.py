import streamlit as st
from src.predictor import predict_points
from src.summarizer import summarize_to_points
from src.preprocessing import preprocess_text

def reset_values():
    st.session_state.reset_values += 1 
    st.session_state.input_text = ""

def run_manual_mode(model, vectorizer):
    with st.expander("Penjelasan"):
        st.write("Pada mode manual ini, anda hanya perlu memasukkan teks berita yang ingin anda baca ke dalam inputan, dan aplikasi akan memproses teks anda dan memberikan poin penting.")
    input_key = f"input_text_{st.session_state.reset_values}"
    input_text = st.text_area("Masukan teks berita secara manual.", height=300, max_chars=30000, key=input_key)

    if st.button("Proses berita"):
        if not input_text.strip():
            st.warning("Masukan teks terlebih dahulu")
            return
        
        summary_points = summarize_to_points(input_text, n_points=3)

        st.subheader("Poin penting pada berita: ")
        final_text = ""
        for point in summary_points:
            st.write(f"- {point}")
            final_text += point + " "

        clean_text = preprocess_text(final_text)

        pred = predict_points(clean_text, model, vectorizer)
        st.success(f"Kategori berita adalah {pred.upper()}")
        st.button ("Kosongkan teks", on_click=reset_values)
