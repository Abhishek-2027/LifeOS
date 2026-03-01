# backend/app/ingestion_engine/ner.py

import spacy

nlp = spacy.load("en_core_web_sm")

class NERExtractor:

    def extract(self, text: str):
        doc = nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]