import requests
import json
import time

# Delay antar akun (detik)
DELAY_PER_ACCOUNT = 2
# Delay antar task (detik)
DELAY_PER_TASK = 1
# Delay jika semua task habis (4 jam = 14400 detik)
DELAY_LOOP = 14400

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

def run_all_accounts(tokens):
    all_done = True

    for i, token in enumerate(tokens):
        print(f"\n=== Akun #{i+1} ===")
        tasks = get_tasks(token)

        if not tasks:
            print("[*] Tidak ada task untuk akun ini.")
        else:
            all_done = False
            for task_id in tasks:
                complete_task(token, task_id)
                time.sleep(DELAY_PER_TASK)

        time.sleep(DELAY_PER_ACCOUNT)

    return all_done

def main():
    try:
        with open("tokens.txt", "r") as f:
            tokens = [line.strip() for line in f if line.strip()]
        if not tokens:
            print("File tokens.txt kosong")
            return

        while True:
            print("\n[🔁] Mulai rotasi akun...")
            semua_habis = run_all_accounts(tokens)

            if semua_habis:
                print(f"\n[⏸️] Semua task sudah habis. Tunggu 4 jam sebelum lanjut...")
                time.sleep(DELAY_LOOP)
            else:
                print("\n[🔄] Selesai satu rotasi. Lanjut ulang rotasi lagi...")

    except KeyboardInterrupt:
        print("\n[!] Dihentikan oleh pengguna")

if __name__ == "__main__":
    main()
