#!/bin/bash
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "[$(date)] Запуск мониторинга..."
python3 "$BASE_DIR/python/collector.py"
python3 "$BASE_DIR/python/alerter.py"
echo "[$(date)] Готово"
