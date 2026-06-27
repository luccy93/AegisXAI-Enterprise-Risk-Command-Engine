import numpy as np


def generate_sentiment_data(seed=42):
    rng = np.random.default_rng(seed)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    monthly_trend = []
    for m in months:
        pos = int(rng.normal(58, 4))
        neg = int(rng.normal(15, 3))
        neu = max(0, 100 - pos - neg)
        monthly_trend.append({"month": m, "positive": pos, "neutral": neu, "negative": neg})

    top_topics = [
        {"topic": "Network Coverage", "count": 342, "sentiment": "Negative"},
        {"topic": "Billing Accuracy", "count": 215, "sentiment": "Neutral"},
        {"topic": "Customer Support", "count": 189, "sentiment": "Positive"},
        {"topic": "Mobile App", "count": 156, "sentiment": "Positive"},
        {"topic": "Pricing", "count": 128, "sentiment": "Negative"},
    ]

    comments_data = [
        ("The network connectivity has been excellent lately.", "Positive", "Happy"),
        ("I am very satisfied with the customer service response time.", "Positive", "Satisfied"),
        ("The billing system keeps making errors on my invoice.", "Negative", "Frustrated"),
        ("Your support team resolved my issue quickly. Thank you!", "Positive", "Happy"),
        ("I am disappointed with the slow internet speeds at peak hours.", "Negative", "Disappointed"),
        ("The mobile app interface is confusing and hard to navigate.", "Negative", "Confused"),
        ("Great value for money. Highly recommend your services.", "Positive", "Happy"),
        ("I have been facing frequent dropped calls lately.", "Negative", "Angry"),
    ]
    recent_comments = [{"comment": c, "sentiment": s, "emotion": e} for c, s, e in comments_data]

    return {
        "overall_sentiment": "Positive",
        "sentiment_distribution": {"Positive": 58, "Neutral": 27, "Negative": 15},
        "emotion_distribution": {"Happy": 32, "Satisfied": 26, "Frustrated": 14, "Angry": 8, "Confused": 12, "Disappointed": 8},
        "monthly_trend": monthly_trend,
        "top_topics": top_topics,
        "recent_comments": recent_comments,
    }


def analyze_comment_sentiment(comment):
    comment_lower = comment.lower()
    positive_words = ["happy", "great", "excellent", "satisfied", "good", "love", "amazing", "thank", "helpful", "fast", "impressed"]
    negative_words = ["bad", "terrible", "awful", "frustrated", "angry", "disappointed", "slow", "poor", "horrible", "worst", "hate"]
    emotion_map = {
        "happy": "Happy", "great": "Happy", "love": "Happy", "amazing": "Happy",
        "excellent": "Satisfied", "satisfied": "Satisfied", "good": "Satisfied", "thank": "Satisfied",
        "frustrated": "Frustrated", "terrible": "Frustrated",
        "angry": "Angry", "hate": "Angry", "horrible": "Angry",
        "confused": "Confused", "confusing": "Confused",
        "disappointed": "Disappointed", "slow": "Disappointed", "poor": "Disappointed",
    }

    pos_score = sum(1 for w in positive_words if w in comment_lower)
    neg_score = sum(1 for w in negative_words if w in comment_lower)

    if pos_score > neg_score:
        sentiment = "Positive"
        score = round(0.5 + (pos_score * 0.1), 2)
    elif neg_score > pos_score:
        sentiment = "Negative"
        score = round(0.5 - (neg_score * 0.1), 2)
    else:
        sentiment = "Neutral"
        score = 0.5

    score = max(0.0, min(1.0, score))

    emotion = "Neutral"
    for word, emo in emotion_map.items():
        if word in comment_lower:
            emotion = emo
            if (sentiment == "Positive" and emo in ("Happy", "Satisfied")) or \
               (sentiment == "Negative" and emo in ("Frustrated", "Angry", "Disappointed", "Confused")):
                break

    return {"sentiment": sentiment, "emotion": emotion, "score": score}
