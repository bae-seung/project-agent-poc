from langchain.tools import tool
from mock_data import TASKS


@tool
def get_blocked_tasks() -> list:
    """
    현재 BLOCKED 상태인 Task 목록을 조회한다.
    """
    return [
        task for task in TASKS
        if task["status"] == "BLOCKED"
    ]


@tool
def get_following_tasks(task_id: int) -> list:
    """
    특정 Task에 직접 의존하는 후속 Task 목록을 조회한다.
    """
    return [
        task for task in TASKS
        if task_id in task["depends_on"]
    ]

@tool
def get_available_tasks() -> list:
    """
    현재 바로 시작할 수 있는 TODO 상태의 Task 목록을 조회한다.
    선행 Task가 모두 DONE 상태이거나 선행 Task가 없는 작업만 반환한다.
    """

    done_task_ids = {
        task["id"]
        for task in TASKS
        if task["status"] == "DONE"
    }

    available_tasks = []

    for task in TASKS:
        if task["status"] != "TODO":
            continue

        dependencies = task["depends_on"]

        if all(
            dependency_id in done_task_ids
            for dependency_id in dependencies
        ):
            available_tasks.append(task)

    return available_tasks