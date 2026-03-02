"""Task constructors for CrewAI workflows.

If ``crewai`` isn’t installed this module can still be imported, but
calling :func:`create_tasks` will raise an informative ``ImportError``.
"""

try:
    from crewai import Task  # type: ignore[import]
    _CREWAI_AVAILABLE = True
except ImportError:  # pragma: no cover
    Task = None
    _CREWAI_AVAILABLE = False


def create_tasks(context):
    if not _CREWAI_AVAILABLE:
        raise ImportError("crewai is not installed; cannot create tasks")

    analysis_task = Task(
        description=f"Analyze this user context:\n{context}",
        expected_output="Behavioral insights and risks."
    )

    planning_task = Task(
        description="Create improvement strategy based on analysis.",
        expected_output="Structured actionable plan."
    )

    execution_task = Task(
        description="Convert strategy into daily executable tasks.",
        expected_output="Clear bullet-point task list."
    )

    return analysis_task, planning_task, execution_task