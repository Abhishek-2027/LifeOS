class DecisionEngine:

    def decide(self, patterns, conflict):

        if conflict:
            return "Resolve emotional conflict before decision."

        if patterns:
            return f"Recurring theme: {patterns[0][0]}"

        return "No major decision required."