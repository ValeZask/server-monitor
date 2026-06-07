import json, os, yaml
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_config():
    with open(os.path.join(BASE_DIR, "config", "config.yaml")) as f:
        return yaml.safe_load(f)

def load_latest_metrics():
    date_str = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(BASE_DIR, "logs", "metrics", f"{date_str}.json")
    with open(path) as f:
        entries = json.load(f)
    return entries[-1]

def check_alerts(metrics, config):
    alerts = []
    cpu = metrics["cpu"]["percent"]
    disk_free = 100 - metrics["disk"]["percent_used"]
    ram = metrics["ram"]["percent"]

    if cpu > config["thresholds"]["cpu_percent"]:
        alerts.append(f"ALERT: CPU {cpu}% > {config['thresholds']['cpu_percent']}%")
    if disk_free < config["thresholds"]["disk_percent_free"]:
        alerts.append(f"ALERT: Диск свободно {disk_free:.1f}% < {config['thresholds']['disk_percent_free']}%")
    if ram > config["thresholds"]["ram_percent"]:
        alerts.append(f"ALERT: RAM {ram}% > {config['thresholds']['ram_percent']}%")
    return alerts

def write_alerts(alerts):
    path = os.path.join(BASE_DIR, "logs", "alerts.log")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a") as f:
        for alert in alerts:
            line = f"{datetime.now().isoformat()} {alert}\n"
            f.write(line)
            print(line.strip())

if __name__ == "__main__":
    config = load_config()
    metrics = load_latest_metrics()
    alerts = check_alerts(metrics, config)
    if alerts:
        write_alerts(alerts)
    else:
        print("Всё в норме, алертов нет")
