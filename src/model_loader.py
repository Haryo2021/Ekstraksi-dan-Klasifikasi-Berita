import joblib
import streamlit as st

@st.cache_resource
def load_model():
    try:
        model = joblib.load("model/model.pkl")
        vectorizer = joblib.load("model/vectorizer.pkl")
        return model, vectorizer
    except Exception as e:
        st.error(f"⚠️ Gagal memuat model/vectorizer: {e}")
        return None, None
