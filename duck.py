import requests
import json
import time

# Delay antar akun (detik)
DELAY_BETWEEN_ACCOUNTS = 5
# Waktu ulang (4 jam = 14400 detik)
LOOP_INTERVAL = 14400

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
            tasks = data.get('payload', {}).get('tasks', [])
            return [task.get('id') for task in tasks if task.get('id')]
        else:
            print(f"[!] Gagal ambil task: {response.status_code}")
            return []
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
            print(f"[+] Task {task_id[:8]} selesai")
            return True
        else:
            print(f"[!] Gagal task {task_id[:8]}: {response.status_code}")
            return False
    except Exception as e:
        print(f"[!] Error task {task_id[:8]}: {e}")
        return False

def run_bot_for_token(token, index):
    print(f"\n=== Akun #{index+1} ===")
    while True:
        tasks = get_tasks(token)
        if not tasks:
            print("[*] Tidak ada task lagi, lanjut akun berikutnya")
            break
        for task_id in tasks:
            complete_task(token, task_id)
            time.sleep(2)  # Delay antar task

def main():
    while True:
        try:
            with open("tokens.txt", "r") as f:
                tokens = [line.strip() for line in f if line.strip()]
            if not tokens:
                print("File tokens.txt kosong")
                break

            for i, token in enumerate(tokens):
                run_bot_for_token(token, i)
                time.sleep(DELAY_BETWEEN_ACCOUNTS)

            print(f"[⏳] Menunggu 4 jam sebelum ulangi lagi...")
            time.sleep(LOOP_INTERVAL)

        except KeyboardInterrupt:
            print("\n[!] Dihentikan oleh pengguna")
            break

if __name__ == "__main__":
    main()
