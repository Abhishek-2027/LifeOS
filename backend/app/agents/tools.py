# backend/app/agents/tools.py

from langchain.tools import tool


@tool
def create_task(task: str) -> str:
    """
    Create a new task in the system with the provided task description.
    """
    return f"Task created: {task}"


@tool
def send_notification(message: str) -> str:
    """
    Send a notification with the given message to the user.
    """
    return f"Notification sent: {message}"


@tool
def prioritize_item(item: str) -> str:
    """
    Mark the given item as high priority in the system.
    """
    return f"Item prioritized: {item}"


def get_tools():
    """
    Return all available agent tools.
    """
    return [create_task, send_notification, prioritize_item]