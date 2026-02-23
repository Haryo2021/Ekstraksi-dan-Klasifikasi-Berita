import requests
from bs4 import BeautifulSoup
import streamlit as st


def scrape_berita(link):
    try:
        response = requests.get(link, timeout=10)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')

        cleaned = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) < 40:
                continue
            if "Baca juga" in text:
                continue
            if "TEMPO.CO" in text:
                continue
            if "Editor" in text:
                continue
            if "Iklan" in text:
                continue
            cleaned.append(text)
        if not cleaned:
            return None

        return " ".join(cleaned)

    except Exception as e:
        st.error(f"⚠️ Gagal mengambil konten dari link: {e}")
        return None
