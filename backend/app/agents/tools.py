# backend/app/agents/tools.py

"""Lightweight replacement for langchain's tool decorator.

The ``@tool`` decorator previously imported from ``langchain.tools``
added unnecessary requirements.  Our agents don't really need its
capabilities (serialization, description metadata, etc.), so we simply
use plain functions.
"""

# No external dependencies are required for these helpers.

def create_task(task: str) -> str:
    """
    Create a new task in the system with the provided task description.
    """
    return f"Task created: {task}"

def send_notification(message: str) -> str:
    """
    Send a notification with the given message to the user.
    """
    return f"Notification sent: {message}"


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