tasks = []

def add_task(title):
    task = {}
    id = len(tasks) + 1

    task['id'] = id
    task['title'] = title
    task['completed'] = True

    tasks.append(task)

    return

def get_tasks():
    return tasks

def find_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

def complete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = True
    return

def delete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return

add_task("Learn Python")
add_task("Learn Git")
add_task("Build FastAPI API")

print(get_tasks())

complete_task(1)

print(get_tasks())