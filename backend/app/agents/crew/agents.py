"""Wrapper for creating CrewAI agents with our in‑house LLM.

The package ``crewai`` is an optional dependency; we don’t force its
installation.  If it isn’t present we allow the module to be imported but
raise when functionality is actually invoked.
"""

try:
    from crewai import Agent  # type: ignore[import]
    _CREWAI_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    Agent = None
    _CREWAI_AVAILABLE = False

from app.reasoning_engine.llm_reasoner import LLMReasoner


def get_llm():
    # keep existing signature so callers need not change
    return LLMReasoner()


def create_agents():
    if not _CREWAI_AVAILABLE:
        raise ImportError(
            "crewai library is not installed; cannot create crew agents"
        )

    llm = get_llm()

    analyst = Agent(
        role="Memory Analyst",
        goal="Analyze user memories and detect behavioral patterns.",
        backstory="Expert in cognitive pattern recognition.",
        llm=llm,
        verbose=True,
    )

    planner = Agent(
        role="Strategic Planner",
        goal="Create structured plans based on memory insights.",
        backstory="Expert in personal productivity optimization.",
        llm=llm,
        verbose=True,
    )

    executor = Agent(
        role="Action Executor",
        goal="Convert plans into actionable steps.",
        backstory="Efficient execution-focused assistant.",
        llm=llm,
        verbose=True,
    )

    return analyst, planner, executor

def create_agents():

    llm = get_llm()

    analyst = Agent(
        role="Memory Analyst",
        goal="Analyze user memories and detect behavioral patterns.",
        backstory="Expert in cognitive pattern recognition.",
        llm=llm,
        verbose=True,
    )

    planner = Agent(
        role="Strategic Planner",
        goal="Create structured plans based on memory insights.",
        backstory="Expert in personal productivity optimization.",
        llm=llm,
        verbose=True,
    )

    executor = Agent(
        role="Action Executor",
        goal="Convert plans into actionable steps.",
        backstory="Efficient execution-focused assistant.",
        llm=llm,
        verbose=True,
    )

    return analyst, planner, executor