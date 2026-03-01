from crewai import Agent
from langchain_community.chat_models import ChatOllama


def get_llm():
    return ChatOllama(model="llama3", temperature=0.3)


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