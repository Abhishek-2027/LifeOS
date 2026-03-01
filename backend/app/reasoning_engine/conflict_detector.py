class ConflictDetector:

    def detect(self, memories):

        texts = [m.text.lower() for m in memories]

        if "confident" in " ".join(texts) and "anxious" in " ".join(texts):
            return "Possible emotional inconsistency detected."

        return None