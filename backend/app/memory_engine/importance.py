# backend/app/memory_engine/importance.py

class ImportanceScorer:

    def score(self, structured_memory: dict):

        score = 0.5

        if structured_memory.get("emotion"):
            score += 0.1

        if structured_memory.get("events"):
            score += 0.1

        if structured_memory.get("temporal"):
            score += 0.1

        return min(score, 1.0)