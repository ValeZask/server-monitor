import json, os, yaml
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_config():
    with open(os.path.join(BASE_DIR, "config", "config.yaml")) as f:
        return yaml.safe_load(f)

def load_metrics_24h():
    metrics_dir = os.path.join(BASE_DIR, "logs", "metrics")
    entries = []
    for i in range(2):
        date_str = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        path = os.path.join(metrics_dir, f"{date_str}.json")
        if os.path.exists(path):
            with open(path) as f:
                entries += json.load(f)
    cutoff = datetime.now() - timedelta(hours=24)
    return [e for e in entries if datetime.fromisoformat(e["timestamp"]) > cutoff]

def color(value, threshold, reverse=False):
    over = value > threshold if not reverse else value < threshold
    return "#ff4d4d" if over else "#4dff88"

def generate_html(entries, config):
    cpu_th = config["thresholds"]["cpu_percent"]
    disk_th = config["thresholds"]["disk_percent_free"]
    ram_th = config["thresholds"]["ram_percent"]

    rows = ""
    for e in entries:
        disk_free = round(100 - e["disk"]["percent_used"], 1)
        cpu_c = color(e["cpu"]["percent"], cpu_th)
        ram_c = color(e["ram"]["percent"], ram_th)
        disk_c = color(disk_free, disk_th, reverse=True)
        rows += f"""
        <tr>
            <td>{e["timestamp"]}</td>
            <td style="background:{cpu_c}">{e["cpu"]["percent"]}%</td>
            <td style="background:{ram_c}">{e["ram"]["percent"]}%</td>
            <td style="background:{disk_c}">{disk_free}%</td>
            <td>{e["disk"]["free_gb"]} GB</td>
        </tr>"""

    total = len(entries)
    avg_cpu = round(sum(e["cpu"]["percent"] for e in entries) / total, 1) if total else 0
    avg_ram = round(sum(e["ram"]["percent"] for e in entries) / total, 1) if total else 0

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Server Monitor Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
        h1 {{ color: #00d4ff; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .card {{ background: #16213e; padding: 20px; border-radius: 8px; min-width: 150px; text-align: center; }}
        .card h3 {{ margin: 0; color: #00d4ff; font-size: 2em; }}
        .card p {{ margin: 5px 0 0; color: #aaa; }}
        table {{ width: 100%; border-collapse: collapse; background: #16213e; border-radius: 8px; overflow: hidden; }}
        th {{ background: #0f3460; padding: 12px; text-align: left; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #0f3460; }}
        tr:last-child td {{ border-bottom: none; }}
        .footer {{ margin-top: 20px; color: #666; font-size: 0.85em; }}
    </style>
</head>
<body>
    <h1>🖥️ Server Monitor — Отчёт за 24 часа</h1>
    <p>Сгенерирован: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

    <div class="summary">
        <div class="card"><h3>{total}</h3><p>Измерений</p></div>
        <div class="card"><h3>{avg_cpu}%</h3><p>Средний CPU</p></div>
        <div class="card"><h3>{avg_ram}%</h3><p>Средний RAM</p></div>
    </div>

    <table>
        <thead><tr><th>Время</th><th>CPU</th><th>RAM</th><th>Диск свободно</th><th>Свободно GB</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
    <div class="footer">🟢 норма &nbsp; 🔴 превышение порога</div>
</body>
</html>"""
    return html

if __name__ == "__main__":
    config = load_config()
    entries = load_metrics_24h()
    html = generate_html(entries, config)
    report_path = os.path.join(BASE_DIR, "logs", "report.html")
    with open(report_path, "w") as f:
        f.write(html)
    print(f"Отчёт сохранён: {report_path} ({len(entries)} записей)")
