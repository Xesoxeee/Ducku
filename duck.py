import requests
import time
import json

# Ambil initData dari file
with open("initdata.txt", "r") as f:
    init_data = f.read().strip()

headers = {
    "accept": "application/json",
    "origin": "https://web.duckystars.app",
    "referer": "https://web.duckystars.app/",
}

# Mendapatkan semua task yang tersedia
def get_all_tasks():
    url = f"https://api.duckystars.app/task/next?initData={init_data}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        tasks = data.get("payload", {}).get("tasks", [])
        print(f"[+] Ditemukan {len(tasks)} task")
        return tasks
    else:
        print("[!] Gagal mengambil task:", response.status_code, response.text)
        return []

# Menyelesaikan task dengan task_id
def complete_task(task_id):
    url = f"https://api.duckystars.app/task/complete?initData={init_data}"
    payload = {"task_id": task_id}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(f"[✓] Task {task_id} selesai")
    else:
        print(f"[!] Gagal menyelesaikan task {task_id}:", response.status_code, response.text)

# Loop utama
while True:
    tasks = get_all_tasks()

    if not tasks:
        print("[-] Tidak ada task tersedia. Tunggu 10 detik...")
        time.sleep(10)
        continue

    for task in tasks:
        task_id = task.get("id")
        code = task.get("code")
        print(f"[>] Kerjakan task: {code} ({task_id})")
        complete_task(task_id)
        time.sleep(5)  # Delay agar task berikutnya bisa muncul

    print("[~] Cek ulang dalam 10 detik...")
    time.sleep(10)
