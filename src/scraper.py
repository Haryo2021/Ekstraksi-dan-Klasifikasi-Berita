import requests
from bs4 import BeautifulSoup
import streamlit as st


def scrape_berita(link):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        
        response = requests.get(link, timeout=15)
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
