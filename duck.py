import requests
import time

# Ambil token dari file
with open("initdata.txt", "r") as f:
    token = f.read().strip()

headers = {
    "authorization": token,
    "accept": "application/json",
    "origin": "https://web.duckystars.app",
    "referer": "https://web.duckystars.app/"
}

def get_next_task():
    url = "https://api.duckystars.app/task/next"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("[+] Next task data:", data)

        tasks = data.get("payload", {}).get("tasks", [])
        if tasks:
            task_id = tasks[0].get("id")
            return task_id
        else:
            return None
    else:
        print("[!] Failed to get task:", response.status_code, response.text)
        return None

def complete_task(task_id):
    url = "https://api.duckystars.app/task/complete"
    payload = {"task_id": task_id}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("[+] Task completed:", task_id)
    else:
        print("[!] Failed to complete task:", response.status_code, response.text)

# Loop auto task
while True:
    task_id = get_next_task()
    if task_id:
        complete_task(task_id)
    else:
        print("[-] No task available, retry in 10s")
        time.sleep(10)
