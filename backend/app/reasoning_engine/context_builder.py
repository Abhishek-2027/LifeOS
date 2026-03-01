# backend/app/reasoning_engine/context_builder.py

class ContextBuilder:

    def build(self, memories):

        return "\n".join(
            [f"{m.text} (importance: {m.importance})" for m in memories]
        )