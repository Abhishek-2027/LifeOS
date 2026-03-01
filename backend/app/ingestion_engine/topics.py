# backend/app/ingestion_engine/topics.py

from sklearn.feature_extraction.text import TfidfVectorizer

class TopicExtractor:

    def extract(self, text: str):

        vectorizer = TfidfVectorizer(stop_words="english", max_features=5)
        X = vectorizer.fit_transform([text])

        return vectorizer.get_feature_names_out().tolist()