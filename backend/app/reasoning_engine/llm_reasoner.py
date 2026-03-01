from langchain_community.chat_models import ChatOllama

class LLMReasoner:

    def __init__(self):
        self.llm = ChatOllama(model="llama3", temperature=0.3)

    def reason(self, context):

        prompt = f"""
        You are a life decision intelligence system.
        Analyze this context:
        {context}

        Provide structured insight.
        """

        return self.llm.invoke(prompt).content