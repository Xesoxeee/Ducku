import requests
import time

class DuckyStarsBot:
    def __init__(self, token, index=1):
        self.token = token
        self.index = index
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            'Accept': "application/json",
            'authorization': self.token,
            'origin': "https://web.duckystars.app",
            'referer': "https://web.duckystars.app/"
        }

    def get_tasks(self):
        url = "https://api.duckystars.app/task/next"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                tasks = data.get("payload", {}).get("tasks", [])
                return [task["id"] for task in tasks]
            elif response.status_code == 404:
                print(f"[{self.index}] ❌ Tidak ada task (404)")
                return []
            else:
                print(f"[{self.index}] ⚠️ Gagal ambil task: {response.status_code}")
                return []
        except Exception as e:
            print(f"[{self.index}] ❌ Error saat ambil task: {e}")
            return []

    def complete_task(self, task_id):
        url = "https://api.duckystars.app/task/complete"
        payload = {"task_id": task_id}
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            data = response.json()
            if data.get("success") or data.get("payload", {}).get("success"):
                print(f"[{self.index}] ✅ Task selesai: {task_id}")
                return True
            else:
                print(f"[{self.index}] ⚠️ Task gagal: {task_id}")
                return False
        except Exception as e:
            print(f"[{self.index}] ❌ Error kirim task: {e}")
            return False

    def run(self):
        total_done = 0
        while True:
            tasks = self.get_tasks()
            if not tasks:
                print(f"[{self.index}] ✅ Semua task selesai ({total_done} task)")
                break

            print(f"[{self.index}] 🔍 Ditemukan {len(tasks)} task")
            for task_id in tasks:
                if self.complete_task(task_id):
                    total_done += 1
                time.sleep(0.7)

            time.sleep(1)  # delay antar batch

if __name__ == "__main__":
    with open("initdata.txt", "r") as f:
        tokens = [line.strip() for line in f if line.strip()]

    for i, token in enumerate(tokens, start=1):
        print(f"\n=============================")
        print(f"🚀 Jalankan akun #{i}")
        print(f"=============================")
        bot = DuckyStarsBot(token, index=i)
        bot.run()
