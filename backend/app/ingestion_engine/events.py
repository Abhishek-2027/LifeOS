# backend/app/ingestion_engine/events.py

from nltk import word_tokenize, pos_tag

class EventExtractor:

    def extract(self, text: str):

        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)

        events = []

        for i in range(len(tagged)-2):
            if tagged[i][1].startswith("VB"):
                phrase = f"{tagged[i-1][0]} {tagged[i][0]} {tagged[i+1][0]}"
                events.append(phrase)

        return events