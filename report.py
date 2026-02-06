import csv
from collections import Counter

FILE_NAME = "feedback_data.csv"

def generate_report():
    ratings = []
    sentiments = Counter()
    negative_words = Counter()
    positive_words = Counter()

    with open(FILE_NAME, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rating = int(row["rating"])
            sentiment = row["sentiment"]
            feedback = row["feedback"].lower()

            ratings.append(rating)
            sentiments[sentiment] += 1

            words = feedback.split()

            if sentiment == "negative":
                negative_words.update(words)
            elif sentiment == "positive":
                positive_words.update(words)

    total = len(ratings)
    avg_rating = round(sum(ratings) / total, 2) if total else 0

    print("\n📊 FEEDBACK SUMMARY REPORT")
    print("-" * 30)
    print(f"Total Responses: {total}")
    print(f"Average Rating: {avg_rating}")
    print(f"Sentiment Distribution: {dict(sentiments)}")

    if negative_words:
        print(f"Top Complaints: {negative_words.most_common(5)}")

    if positive_words:
        print(f"Top Strengths: {positive_words.most_common(5)}")

    print("\n🧠 Conclusion:")
    if avg_rating < 3:
        print("⚠️ Customer satisfaction is low. Immediate action recommended.")
    else:
        print("✅ Customer satisfaction is healthy. Keep up the good work.")
