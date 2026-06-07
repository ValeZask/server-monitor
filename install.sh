#!/bin/bash
set -e
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "=== Server Monitor — Установка ==="

# Проверка зависимостей
for cmd in python3 pip3 tar; do
    command -v $cmd &>/dev/null && echo "✓ $cmd найден" || { echo "✗ $cmd не найден, установи его"; exit 1; }
done

# Установка Python пакетов
echo "Устанавливаю Python зависимости..."
pip3 install -r "$BASE_DIR/requirements.txt" -q
echo "✓ Зависимости установлены"

# Создание папок
mkdir -p "$BASE_DIR/logs/metrics"
echo "✓ Папки созданы"

# Права на скрипты
chmod +x "$BASE_DIR/scripts/"*.sh
echo "✓ Права на скрипты выданы"

# Настройка путей бэкапа
read -p "Папка для хранения бэкапов [/home/$USER/backups]: " BACKUP_DEST
BACKUP_DEST="${BACKUP_DEST:-/home/$USER/backups}"
mkdir -p "$BACKUP_DEST"

# Обновляем config.yaml
sed -i "s|destination:.*|destination: $BACKUP_DEST|" "$BASE_DIR/config/config.yaml"
echo "✓ Путь бэкапов: $BACKUP_DEST"

# Предложение настроить cron
echo ""
echo "Добавить задачи в cron? (y/n)"
read -p "> " ADD_CRON
if [[ "$ADD_CRON" == "y" ]]; then
    (crontab -l 2>/dev/null; cat "$BASE_DIR/crontab.example") | crontab -
    echo "✓ Cron настроен"
fi

echo ""
echo "=== Установка завершена ==="
echo "Запуск: bash scripts/monitor.sh"
echo "Отчёт:  python3 python/report_generator.py"
