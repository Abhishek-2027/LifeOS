from crewai import Task


def create_tasks(context):

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