# backend/app/reasoning_engine/llm_reasoner.py

import requests


class LLMReasoner:

    def __init__(self, model_name: str = "llama3"):
        self.model = model_name
        self.base_url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        try:
            response = requests.post(
                self.base_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )

            response.raise_for_status()

            return response.json().get("response", "")

        except Exception as e:
            return f"LLM Error: {str(e)}"

    # convenience wrapper used by reasoning_service and agents
    def reason(self, context: str, trends: str, conflict: str, decision: str, user_query: str) -> str:
        prompt = (
            "You are an intelligent reasoning engine. "
            "Use the information below to craft a comprehensive explanation.\n\n"
            f"Context: {context}\n"
            f"Trends: {trends}\n"
            f"Conflict: {conflict}\n"
            f"Decision: {decision}\n"
            f"User query: {user_query}\n\n"
            "Provide a clear, step-by-step rationale for the decision "
            "and any recommendations you would offer."
        )
        return self.generate(prompt)