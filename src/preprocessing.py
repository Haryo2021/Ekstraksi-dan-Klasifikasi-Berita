import re
import string

def clean_text_safe(text):
    if not isinstance(text, str):
        text = str(text)

    text = text.replace('\x00', '')
    text = text.replace('…', '...')
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n+', '\n', text)
    return text.strip()

def preprocess_text(text):
    if not isinstance(text, str):
        text = str(text)
    text = clean_text_safe(text)
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()
