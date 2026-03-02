from langchain_community.chat_models import ChatOllama


class LLMReasoner:

    def __init__(self):
        self.llm = ChatOllama(
            model="llama3",
            temperature=0.3
        )

    def reason(self, context, trends, conflict, decision, user_query):

        prompt = f"""
        You are LifeOS, a cognitive decision intelligence system.

        User Query:
        {user_query}

        Retrieved Memory Context:
        {context}

        Behavioral Trends:
        {trends}

        Conflict Analysis:
        {conflict}

        Preliminary Decision:
        {decision}

        Provide deep, structured reasoning and actionable advice.
        """

        return self.llm.invoke(prompt).content