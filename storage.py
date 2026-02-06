all_responses = []

def save_conversation(conversation_data):
    all_responses.append(conversation_data)

def get_all_conversations():
    return all_responses


import csv
import os

FILE_NAME = "feedback_data.csv"

FIELDS = [
    "rating",
    "sentiment",
    "feedback",
    "follow_up",
    "suggestions"
]

def save_to_csv(data):
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "rating": data.get("rating"),
            "sentiment": data.get("sentiment"),
            "feedback": data.get("feedback"),
            "follow_up": data.get("follow_up"),
            "suggestions": data.get("suggestions")
        })
