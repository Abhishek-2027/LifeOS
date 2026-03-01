# backend/app/reasoning_engine/trend_analyzer.py

from collections import defaultdict, Counter
from datetime import datetime
import statistics


class TrendAnalyzer:
    """
    Advanced behavioral trend analyzer.
    Detects:
    - Emotional drift
    - Recurring themes
    - Behavioral escalation
    - Cognitive volatility
    - Episodic vs Semantic dominance
    """

    def analyze(self, memories):

        if not memories:
            return {"message": "No memory data available."}

        # Separate memory types
        episodic = [m for m in memories if m.memory_type == "episodic"]
        semantic = [m for m in memories if m.memory_type == "semantic"]

        # --------------------------
        # 1️⃣ Emotional Timeline
        # --------------------------

        emotion_over_time = defaultdict(list)

        for m in episodic:
            if m.emotion:
                date = m.created_at.date()
                emotion_over_time[date].append(m.emotion)

        emotion_summary = {
            str(date): Counter(emotions)
            for date, emotions in emotion_over_time.items()
        }

        # --------------------------
        # 2️⃣ Dominant Emotions
        # --------------------------

        all_emotions = [
            m.emotion for m in memories if m.emotion
        ]

        dominant_emotions = Counter(all_emotions).most_common(3)

        # --------------------------
        # 3️⃣ Topic Recurrence
        # --------------------------

        topic_counter = Counter()

        for m in semantic:
            words = m.text.lower().split()
            topic_counter.update(words)

        top_recurring_topics = topic_counter.most_common(5)

        # --------------------------
        # 4️⃣ Behavioral Escalation Detection
        # --------------------------

        # Check if negative emotions increase over time
        negative_keywords = ["anxious", "fear", "stress", "failure", "sad"]

        escalation_score = 0

        for m in episodic:
            if m.emotion and m.emotion.lower() in negative_keywords:
                escalation_score += 1

        escalation_ratio = escalation_score / max(len(episodic), 1)

        # --------------------------
        # 5️⃣ Cognitive Volatility
        # --------------------------

        importance_values = [m.importance for m in memories if m.importance]

        volatility = (
            statistics.pstdev(importance_values)
            if len(importance_values) > 1
            else 0
        )

        # --------------------------
        # 6️⃣ Repeated Failure Patterns
        # --------------------------

        failure_patterns = [
            m.text for m in memories
            if "fail" in m.text.lower() or "rejected" in m.text.lower()
        ]

        # --------------------------
        # 7️⃣ Temporal Density
        # --------------------------

        dates = [m.created_at.date() for m in memories]
        density = Counter(dates)

        peak_activity_days = density.most_common(3)

        # --------------------------
        # 8️⃣ Behavioral Loop Detection
        # --------------------------

        # Detect repeated phrases
        phrase_counter = Counter()

        for m in memories:
            tokens = m.text.lower().split()
            for token in tokens:
                if len(token) > 4:
                    phrase_counter[token] += 1

        repeated_tokens = [
            token for token, count in phrase_counter.items()
            if count > 3
        ]

        # --------------------------
        # Final Structured Output
        # --------------------------

        return {
            "dominant_emotions": dominant_emotions,
            "emotion_timeline": emotion_summary,
            "top_recurring_topics": top_recurring_topics,
            "escalation_ratio": round(escalation_ratio, 3),
            "cognitive_volatility": round(volatility, 3),
            "failure_patterns": failure_patterns[:5],
            "peak_activity_days": peak_activity_days,
            "repeated_behavioral_tokens": repeated_tokens[:5],
            "episodic_count": len(episodic),
            "semantic_count": len(semantic),
        }