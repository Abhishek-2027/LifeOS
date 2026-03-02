# backend/app/services/embedding_service.py

import requests
import json
import os
from typing import List

# Ollama embeddings endpoint
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
EMBEDDING_MODEL = "nomic-embed-text"  # Free, good model

class EmbeddingService:
    
    @staticmethod
    async def get_embedding(text: str) -> List[float]:
        """Get embedding for text from Ollama"""
        try:
            # Try to get embedding from Ollama
            response = requests.post(
                f"{OLLAMA_URL}/api/embeddings",
                json={"model": EMBEDDING_MODEL, "prompt": text},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("embedding", [])
            else:
                print(f"Ollama embeddings error: {response.status_code}")
                # Fallback: return None to use text search instead
                return None
        except Exception as e:
            print(f"Embedding service error: {e}")
            return None

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if not vec1 or not vec2:
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = sum(a * a for a in vec1) ** 0.5
        mag2 = sum(b * b for b in vec2) ** 0.5
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
