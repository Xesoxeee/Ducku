import requests
import json
import time

MAX_TASK_PER_ACCOUNT = 10
LOOP_INTERVAL = 4 * 60 * 60  # 4 jam
TASK_INTERVAL = 2  # delay antar task
DELAY_BETWEEN_ACCOUNTS = 1  # delay antar akun

def get_tasks(token):
    headers = {
        'Authorization': token,
        'Accept': 'application/json',
        'Origin': 'https://web.duckystars.app',
        'Referer': 'https://web.duckystars.app/',
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        response = requests.get('https://api.duckystars.app/task/next', headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [t['id'] for t in data.get('payload', {}).get('tasks', [])]
        else:
            print(f"[!] Gagal ambil task (token terblokir?): {response.status_code}")
    except Exception as e:
        print(f"[!] Error ambil task: {e}")
    return []

def complete_task(token, task_id):
    headers = {
        'Authorization': token,
        'Accept': 'application/json',
        'Origin': 'https://web.duckystars.app',
        'Referer': 'https://web.duckystars.app/',
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json'
    }
    payload = {"task_id": task_id}
    try:
        response = requests.post("https://api.duckystars.app/task/complete", headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"[✓] Task {task_id[:8]} selesai")
            return True
        else:
            print(f"[!] Gagal task {task_id[:8]}: {response.status_code}")
    except Exception as e:
        print(f"[!] Error task {task_id[:8]}: {e}")
    return False

def run_once_all_accounts(tokens):
    total_task = 0
    for i, token in enumerate(tokens):
        print(f"\n==> Akun #{i+1}")
        tasks = get_tasks(token)
        if not tasks:
            print("[-] Tidak ada task")
            continue
        for j, task_id in enumerate(tasks[:MAX_TASK_PER_ACCOUNT]):
            complete_task(token, task_id)
            total_task += 1
            time.sleep(TASK_INTERVAL)
        time.sleep(DELAY_BETWEEN_ACCOUNTS)
    return total_task

def main():
    try:
        with open("tokens.txt", "r") as f:
            tokens = [line.strip() for line in f if line.strip()]
        if not tokens:
            print("File tokens.txt kosong.")
            return
    except FileNotFoundError:
        print("File tokens.txt tidak ditemukan.")
        return

    while True:
        print("\n=== Menjalankan 1 loop semua akun ===")
        total_task_done = run_once_all_accounts(tokens)

        if total_task_done == 0:
            print("[🕒] Tidak ada task ditemukan. Menunggu 4 jam...\n")
            time.sleep(LOOP_INTERVAL)
        else:
            print(f"[✔] Selesai {total_task_done} task. Ulangi loop segera...\n")

if __name__ == "__main__":
    main()
