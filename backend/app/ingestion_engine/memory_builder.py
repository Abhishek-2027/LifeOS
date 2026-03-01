# backend/app/ingestion_engine/memory_builder.py

from .ner import NERExtractor
from .temporal import TemporalExtractor
from .events import EventExtractor
from .emotions import EmotionDetector
from .topics import TopicExtractor


class MemoryBuilder:

    def __init__(self):
        self.ner = NERExtractor()
        self.temporal = TemporalExtractor()
        self.events = EventExtractor()
        self.emotion = EmotionDetector()
        self.topics = TopicExtractor()

    def build(self, text: str):

        return {
            "raw_text": text,
            "entities": self.ner.extract(text),
            "temporal": self.temporal.extract(text),
            "events": self.events.extract(text),
            "emotion": self.emotion.detect(text),
            "topics": self.topics.extract(text),
        }