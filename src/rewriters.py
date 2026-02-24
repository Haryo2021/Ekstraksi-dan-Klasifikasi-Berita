import nltk
import streamlit as st
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
torch.manual_seed(42)

MODEL_NAME = "cahya/bert2bert-indonesian-summarization"

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    
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

    import nltk
    sentences = nltk.sent_tokenize(text)
    text = " ".join(sentences[:5])

    tokenizer, model = load_model()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

summary_ids = model.generate(
    inputs["input_ids"],
    min_length=30,
    max_length=120,
    do_sample=True,
    temperature=0.7,
    top_k=50,
    top_p=0.9,
    repetition_penalty=2.0,
    no_repeat_ngram_size=3
)

    rewritten = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return post_process_text(rewritten)


