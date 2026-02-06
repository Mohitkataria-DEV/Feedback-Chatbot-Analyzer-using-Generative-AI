def generate_recommendations(analytics):
    recommendations = []

    sentiment_dist = analytics.get("sentiment_distribution", {})
    avg_rating = analytics.get("average_rating", 0)
    negative_keywords = analytics.get("top_negative_keywords", [])
    positive_keywords = analytics.get("top_positive_keywords", [])

    # Rule 1: Overall dissatisfaction
    if sentiment_dist.get("negative", 0) > sentiment_dist.get("positive", 0):
        recommendations.append(
            "Overall sentiment is negative. Immediate investigation required."
        )

    # Rule 2: Low average rating
    if avg_rating and avg_rating < 3:
        recommendations.append(
            f"Average rating is low ({avg_rating}). Prioritize service improvements."
        )

    # Rule 3: Repeated issues
    if negative_keywords:
        top_issue = negative_keywords[0][0]
        recommendations.append(
            f"Most common complaint relates to '{top_issue}'. Address this first."
        )

    # Rule 4: Strengths
    if positive_keywords:
        top_strength = positive_keywords[0][0]
        recommendations.append(
            f"Users frequently mention '{top_strength}' positively. Maintain this strength."
        )

    if not recommendations:
        recommendations.append(
            "Feedback is generally positive. Continue monitoring for trends."
        )

    return recommendations
