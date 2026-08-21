import requests

response = requests.get("https://jsonplaceholder.typicode.com/todos/1")

if response.status_code == 200:
    data = response.json()

    print(f"Task: {data['title']}")
    print(f"Completed: {data['completed']}")
else:
    print("Failed to retrieve task.")