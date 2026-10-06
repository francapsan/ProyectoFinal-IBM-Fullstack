import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

EXPRESS_URL = getattr(settings, 'EXPRESS_SERVICE_URL', 'http://127.0.0.1:3030')
SENTIMENT_URL = getattr(settings, 'SENTIMENT_SERVICE_URL', 'http://127.0.0.1:5000')

def get_dealers(state=None):
    """
    Fetch all dealerships, or dealerships filtered by state.
    """
    try:
        if state and state.strip() and state.lower() != 'all':
            url = f"{EXPRESS_URL}/dealers/{state.strip()}"
        else:
            url = f"{EXPRESS_URL}/dealers"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        logger.warning(f"Express service returned {response.status_code} for {url}")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to Express service at {EXPRESS_URL}: {e}")
        return []

def get_dealer_by_id(dealer_id):
    """
    Fetch specific dealership by numeric ID.
    """
    try:
        url = f"{EXPRESS_URL}/dealer/{dealer_id}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        logger.warning(f"Express service returned {response.status_code} for dealer {dealer_id}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching dealer {dealer_id}: {e}")
        return None

def get_reviews_by_dealer_id(dealer_id):
    """
    Fetch reviews for a specific dealership.
    """
    try:
        url = f"{EXPRESS_URL}/reviews/dealer/{dealer_id}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            reviews = response.json()
            # Enrich reviews with sentiment analysis
            for r in reviews:
                review_text = r.get('review', '')
                sentiment_data = analyze_sentiment(review_text)
                r['sentiment'] = sentiment_data.get('sentiment', 'neutral')
                r['compound_score'] = sentiment_data.get('compound_score', 0.0)
            return reviews
        logger.warning(f"Express service returned {response.status_code} for reviews")
        return []
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching reviews for dealer {dealer_id}: {e}")
        return []

def analyze_sentiment(text):
    """
    Call sentiment analyzer microservice to classify review sentiment.
    """
    if not text:
        return {'sentiment': 'neutral', 'compound_score': 0.0}
    try:
        url = f"{SENTIMENT_URL}/analyze"
        response = requests.get(url, params={'text': text}, timeout=4)
        if response.status_code == 200:
            return response.json()
        logger.warning(f"Sentiment service returned status {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error contacting sentiment service at {SENTIMENT_URL}: {e}")
    
    # Fallback heuristic if microservice is down
    lower = text.lower()
    positive_words = ['great', 'excellent', 'amazing', 'exceptional', 'loved', 'good', 'best', 'friendly']
    negative_words = ['bad', 'terrible', 'worst', 'poor', 'disappointed', 'awful', 'denied', 'horrible']
    
    pos_matches = sum(1 for w in positive_words if w in lower)
    neg_matches = sum(1 for w in negative_words if w in lower)
    
    if pos_matches > neg_matches:
        return {'sentiment': 'positive', 'compound_score': 0.5}
    elif neg_matches > pos_matches:
        return {'sentiment': 'negative', 'compound_score': -0.5}
    return {'sentiment': 'neutral', 'compound_score': 0.0}

def post_review(review_data):
    """
    Post a new customer review to Express/Mongo service.
    """
    try:
        url = f"{EXPRESS_URL}/insert_review"
        response = requests.post(url, json=review_data, timeout=5)
        if response.status_code in [200, 201]:
            return response.json()
        logger.error(f"Failed to post review: {response.status_code} - {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error posting review to {url}: {e}")
        return None
