from collections import Counter

def generate_analytics(conversations):
    total = len(conversations)

    if total == 0:
        return {}

    sentiment_counts = Counter()
    ratings = []
    common_issues = Counter()
    positives = Counter()

    for convo in conversations:
        sentiment = convo.get("sentiment")
        rating = convo.get("rating")
        feedback = convo.get("feedback", "").lower()

        if sentiment:
            sentiment_counts[sentiment] += 1

        if rating:
            ratings.append(rating)

        if sentiment == "negative":
            common_issues.update(feedback.split())

        if sentiment == "positive":
            positives.update(feedback.split())

    avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

    return {
        "total_responses": total,
        "average_rating": avg_rating,
        "sentiment_distribution": dict(sentiment_counts),
        "top_negative_keywords": common_issues.most_common(5),
        "top_positive_keywords": positives.most_common(5)
    }
