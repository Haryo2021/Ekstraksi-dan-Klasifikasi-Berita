import nltk
import streamlit as st
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "cahya/bert2bert-indonesian-summarization"

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    return tokenizer, model



def post_process_text(text):
    if not text: return ""

    text = text.strip()
    if len(text) > 0:
        text = text[0].upper() + text[1:]

    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)
    text = re.sub(r'\s+/\s+', '/', text)

    return text


def rewrite_list_of_sentences(text):
    if not isinstance(text, str):
        text = str(text)

    tokenizer, model = load_model()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    summary_ids = model.generate(
        inputs["input_ids"],
        min_length=20,
        max_length=80,
        num_beams=4,
        early_stopping=True
    )

    rewritten = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return post_process_text(rewritten)
