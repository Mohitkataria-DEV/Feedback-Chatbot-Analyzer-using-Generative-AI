

        # Dynamic follow-up based on sentiment
        if self.state in [
            "FOLLOW_UP_NEGATIVE",
            "FOLLOW_UP_POSITIVE",
            "FOLLOW_UP_NEUTRAL"
        ]:

            if not user_input or user_input.strip() == "":