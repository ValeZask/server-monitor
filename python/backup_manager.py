import os, tarfile, json, yaml
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_config():
    with open(os.path.join(BASE_DIR, "config", "config.yaml")) as f:
        return yaml.safe_load(f)

def create_backup(sources, destination):
    os.makedirs(destination, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"backup_{timestamp}.tar.gz"
    archive_path = os.path.join(destination, archive_name)

    with tarfile.open(archive_path, "w:gz") as tar:
        for source in sources:
            if os.path.exists(source):
                tar.add(source, arcname=os.path.basename(source))
                print(f"  + добавлен: {source}")
            else:
                print(f"  ! не найден (пропущен): {source}")

    size_mb = round(os.path.getsize(archive_path) / 1e6, 2)
    print(f"Архив создан: {archive_path} ({size_mb} MB)")
    return archive_path, size_mb

def rotate_backups(destination, keep_last):
    backups = sorted([
        f for f in os.listdir(destination)
        if f.startswith("backup_") and f.endswith(".tar.gz")
    ])
    to_delete = backups[:-keep_last] if len(backups) > keep_last else []
    for old in to_delete:
        os.remove(os.path.join(destination, old))
        print(f"Удалён старый бэкап: {old}")
    return len(to_delete)

def write_log(archive_path, size_mb, sources, deleted_count, status):
    log_path = os.path.join(BASE_DIR, "logs", "backup_history.json")
    entries = []
    if os.path.exists(log_path):
        with open(log_path) as f:
            entries = json.load(f)
    entries.append({
        "timestamp": datetime.now().isoformat(),
        "archive": os.path.basename(archive_path),
        "size_mb": size_mb,
        "sources": sources,
        "deleted_old_backups": deleted_count,
        "status": status
    })
    with open(log_path, "w") as f:
        json.dump(entries, f, indent=2)

if __name__ == "__main__":
    config = load_config()
    sources = config["backup"]["sources"]
    destination = config["backup"]["destination"]
    keep_last = config["backup"]["keep_last"]

    try:
        archive_path, size_mb = create_backup(sources, destination)
        deleted = rotate_backups(destination, keep_last)
        write_log(archive_path, size_mb, sources, deleted, "success")
        print("Бэкап завершён успешно")
    except Exception as e:
        print(f"Ошибка: {e}")
        write_log("", 0, sources, 0, f"error: {e}")
