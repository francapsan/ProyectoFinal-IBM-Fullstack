from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

app = Flask(__name__)
CORS(app)

# Ensure NLTK vader_lexicon is downloaded
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

sid = SentimentIntensityAnalyzer()

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "online",
        "service": "Car Dealership Sentiment Analyzer Microservice",
        "version": "1.0.0",
        "endpoints": {
            "GET /analyze?text=<text>": "Analyze text sentiment via query parameter",
            "POST /analyze": "Analyze JSON payload {\"text\": \"<text>\"}"
        }
    }), 200

@app.route("/analyze", methods=["GET", "POST"])
def analyze_sentiment():
    text = ""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        text = data.get("text", "")
    else:
        text = request.args.get("text", "")

    if not text:
        return jsonify({
            "error": "Missing 'text' parameter",
            "sentiment": "neutral",
            "score": 0.0
        }), 400

    scores = sid.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "positive"
    elif compound <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return jsonify({
        "status": 200,
        "text": text,
        "sentiment": sentiment,
        "compound_score": compound,
        "scores": scores
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
