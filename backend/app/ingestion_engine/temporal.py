# backend/app/ingestion_engine/temporal.py

import spacy

nlp = spacy.load("en_core_web_sm")

class TemporalExtractor:

    def extract(self, text: str):
        doc = nlp(text)
        return [ent.text for ent in doc.ents if ent.label_ in ["DATE", "TIME"]]