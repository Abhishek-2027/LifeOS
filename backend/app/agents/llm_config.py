# backend/app/agents/llm_config.py

"""Return a simple LLM client without pulling in langchain/crewai.

Other modules in the repository call :func:`get_llm` to obtain an object
that exposes a ``generate`` or ``invoke`` style interface.  We used to
return ``ChatOllama`` from langchain_community, but that required
installing langchain and introduced the version conflicts described in
user reports.  Instead, we use our own LLMReasoner which talks to the
local HTTP model endpoint.
"""

from app.reasoning_engine.llm_reasoner import LLMReasoner


def get_llm() -> LLMReasoner:
    return LLMReasoner()