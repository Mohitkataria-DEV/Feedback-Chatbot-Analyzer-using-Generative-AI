from states import STATES
from sentiment import analyze_sentiment
from scaledown import should_scaledown


class Conversation:
    def __init__(self):
        self.state = "GREETING"
        self.responses = {
            "rating": None,
            "sentiment": None,
            "feedback": None,
            "follow_up": None,
            "suggestions": None
        }

    def next(self, user_input=None):

        # GREETING → ASK_RATING
        if self.state == "GREETING":
            self.state = "ASK_RATING"
            return f'{STATES["GREETING"]}\n{STATES["ASK_RATING"]}'

        # ASK_RATING
        if self.state == "ASK_RATING":

            if not user_input or user_input.strip() == "":
                return "Please enter a number between 1 and 5."

            if not user_input.isdigit():
                return "Invalid input. Please enter a number between 1 and 5."

            rating = int(user_input)

            if rating < 1 or rating > 5:
                return "Please enter a number between 1 and 5."

            self.responses["rating"] = rating

            if rating <= 3:
                self.state = "ASK_NEGATIVE"
                return STATES["ASK_NEGATIVE"]
            else:
                self.state = "ASK_POSITIVE"
                return STATES["ASK_POSITIVE"]

        # Initial feedback
        if self.state in ["ASK_NEGATIVE", "ASK_POSITIVE"]:

            if not user_input or user_input.strip() == "":
                return "Response cannot be empty. Please share your feedback."

            sentiment = analyze_sentiment(user_input)

            self.responses["feedback"] = user_input
            self.responses["sentiment"] = sentiment

            if sentiment == "negative":
                self.state = "FOLLOW_UP_NEGATIVE"
                return STATES["FOLLOW_UP_NEGATIVE"]
            elif sentiment == "positive":
                self.state = "FOLLOW_UP_POSITIVE"
                return STATES["FOLLOW_UP_POSITIVE"]
            else:
                self.state = "FOLLOW_UP_NEUTRAL"
                return STATES["FOLLOW_UP_NEUTRAL"]

        # Follow-up step
        if self.state in [
            "FOLLOW_UP_NEGATIVE",
            "FOLLOW_UP_POSITIVE",
            "FOLLOW_UP_NEUTRAL"
        ]:

            if not user_input or user_input.strip() == "":
                return "Please share your thoughts."

            self.responses["follow_up"] = user_input

            # 🔒 Ensure suggestions always exist
            self.responses.setdefault("suggestions", "None")

            # Apply ScaleDown AFTER storing data
            if should_scaledown(self.responses):
                self.state = "END"
                return STATES["END"]

            self.state = "ASK_SUGGESTIONS"
            return STATES["ASK_SUGGESTIONS"]

        # Suggestions
        if self.state == "ASK_SUGGESTIONS":

            if not user_input or user_input.strip() == "":
                return "Please enter your suggestion (or type 'None')."

            self.responses["suggestions"] = user_input
            self.state = "END"
            return STATES["END"]

        return None
