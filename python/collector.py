import psutil, json, os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_metrics():
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu": {"percent": psutil.cpu_percent(interval=1)},
        "ram": {"percent": psutil.virtual_memory().percent, "total_gb": round(psutil.virtual_memory().total / 1e9, 2)},
        "disk": {"percent_used": psutil.disk_usage("/").percent, "free_gb": round(psutil.disk_usage("/").free / 1e9, 2)},
        "services": [p.name() for p in psutil.process_iter() if p.status() == "running"][:10]
    }

def save_metrics(metrics):
    date_str = datetime.now().strftime("%Y-%m-%d")
    metrics_dir = os.path.join(BASE_DIR, "logs", "metrics")
    os.makedirs(metrics_dir, exist_ok=True)
    path = os.path.join(metrics_dir, f"{date_str}.json")
    entries = []
    if os.path.exists(path):
        with open(path) as f:
            entries = json.load(f)
    entries.append(metrics)
    with open(path, "w") as f:
        json.dump(entries, f, indent=2)
    print(f"Метрики сохранены: {path}")

if __name__ == "__main__":
    m = get_metrics()
    save_metrics(m)
