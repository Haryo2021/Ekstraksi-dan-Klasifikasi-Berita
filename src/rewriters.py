import nltk
import re
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

pipe = pipeline("summarization", model="cahya/bert2bert-indonesian-summarization")


try:
    tokenizer = AutoTokenizer.from_pretrained("cahya/bert2bert-indonesian-summarization")
    model = AutoModelForSeq2SeqLM.from_pretrained("cahya/bert2bert-indonesian-summarization")                                 
except Exception as e:
    print(f"Error loading model: {e}")

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

    input_ids = tokenizer.encode(text, return_tensors="pt", max_length=512, truncation=True)

    summary_ids = model.generate(
        input_ids,
        min_length=20,
        max_length=80,
        num_beams=8,
        repetition_penalty=2.5,
        no_repeat_ngram_size=3,
        early_stopping=True
    )

    rewritten = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    final_result = post_process_text(rewritten)

    return final_result