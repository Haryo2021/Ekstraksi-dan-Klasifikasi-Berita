from src.preprocessing import preprocess_text

def predict_points(text, model, vectorizer):
    clean_text = preprocess_text(text)
    X = vectorizer.transform([clean_text])
    prediction = model.predict(X)
    return prediction[0]
