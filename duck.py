import requests
import json
import time

class DuckyStarsBot:
    def __init__(self, token, index):
        self.token = token
        self.task_ids = []
        self.request_count = 0
        self.successful_requests = 0
        self.index = index

    def get_tasks(self):
        """Ambil semua task"""
        url = "https://api.duckystars.app/task/next"
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            'Accept': "application/json",
            'authorization': self.token,
            'origin': "https://web.duckystars.app",
            'referer': "https://web.duckystars.app/"
        }

        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code != 200:
                print(f"[{self.index}] ❌ Gagal ambil task. Status: {res.status_code}")
                return []
            
            data = res.json()
            tasks = data.get('payload', {}).get('tasks', [])
            self.task_ids = [task['id'] for task in tasks]
            print(f"[{self.index}] ✅ Total task: {len(self.task_ids)}")
            return self.task_ids
        
        except Exception as e:
            print(f"[{self.index}] ❌ Error ambil task: {e}")
            return []

    def complete_task(self, task_id):
        """Selesaikan task"""
        url = "https://api.duckystars.app/task/complete"
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            'Accept': "application/json",
            'Content-Type': "application/json",
            'authorization': self.token,
            'origin': "https://web.duckystars.app",
            'referer': "https://web.duckystars.app/"
        }
        payload = {"task_id": task_id}

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=10)
            data = res.json()
            success = data.get('payload', {}).get('success', False)
            self.request_count += 1
            if success:
                self.successful_requests += 1
                print(f"[{self.index}] ✅ Task sukses: {task_id[:8]}")
            else:
                print(f"[{self.index}] ❌ Task gagal: {task_id[:8]}")
        except Exception as e:
            print(f"[{self.index}] ❌ Error: {e}")

    def run(self):
        print(f"\n🚀 Mulai akun #{self.index}")
        tasks = self.get_tasks()
        if not tasks:
            print(f"[{self.index}] ⚠️ Tidak ada task.")
            return
        
        for idx, task_id in enumerate(tasks, 1):
            print(f"[{self.index}] ➡️ Task {idx}/{len(tasks)}")
            self.complete_task(task_id)
            time.sleep(0.5)

        print(f"\n[{self.index}] ✅ Semua task selesai. Sukses: {self.successful_requests}/{self.request_count}\n")

def load_tokens(filename="tokens.txt"):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    tokens = load_tokens()
    if not tokens:
        print("❌ Tidak ada token ditemukan di 'tokens.txt'")
        return
    
    for idx, token in enumerate(tokens, 1):
        bot = DuckyStarsBot(token, idx)
        bot.run()
        time.sleep(2)  # Jeda antar akun (hindari spam API)

if __name__ == "__main__":
    main()
