# backend/app/agents/tools.py

from langchain.tools import tool


@tool
def create_task(task: str) -> str:
    return f"Task created: {task}"


@tool
def send_notification(message: str) -> str:
    return f"Notification sent: {message}"


@tool
def prioritize_item(item: str) -> str:
    return f"Item prioritized: {item}"


def get_tools():
    return [create_task, send_notification, prioritize_item]