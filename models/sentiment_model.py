from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="w11wo/indonesian-roberta-base-sentiment-classifier"
)

def predict_sentiment(text):

    result = classifier(text)

    label = result[0]['label']

    if label == "positive":
        return "Positif"

    elif label == "negative":
        return "Negatif"

    else:
        return "Netral"