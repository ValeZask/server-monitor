#!/bin/bash
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_FILE="$BASE_DIR/logs/backup.log"

echo "[$(date)] Запуск бэкапа..." | tee -a "$LOG_FILE"
python3 "$BASE_DIR/python/backup_manager.py" 2>&1 | tee -a "$LOG_FILE"
echo "[$(date)] Бэкап завершён" | tee -a "$LOG_FILE"
