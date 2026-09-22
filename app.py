from tools import (
    get_blocked_tasks,
    get_following_tasks,
    get_available_tasks
)


print("BLOCKED Task:")
print(get_blocked_tasks.invoke({}))

print("\nTask 1의 후속 Task:")
print(
    get_following_tasks.invoke({
        "task_id": 1
    })
)

print("\n현재 바로 시작 가능한 Task:")
print(get_available_tasks.invoke({}))