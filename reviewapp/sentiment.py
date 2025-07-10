from textblob import TextBlob

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity
