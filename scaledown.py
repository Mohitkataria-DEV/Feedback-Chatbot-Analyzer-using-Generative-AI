def should_scaledown(responses):
    rating = responses.get("rating")
    sentiment = responses.get("sentiment")

    # Very happy users
    if rating == 5 and sentiment == "positive":
        return True

    # Very unhappy users
    if rating == 1 and sentiment == "negative":
        return True

    # Extreme rating but neutral text
    if rating in [1, 5] and sentiment == "neutral":
        return True

    return False
