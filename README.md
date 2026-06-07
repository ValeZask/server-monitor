# 🖥️ Server Monitor

Система мониторинга сервера с алертами, автобэкапом и HTML отчётами.

## Что делает

- **Мониторинг** CPU, RAM, диска каждые 5 минут
- **Алерты** в `logs/alerts.log` при превышении порогов
- **Автобэкап** папок в `.tar.gz` каждую ночь в 02:00
- **Ротация** — хранит только 7 последних бэкапов
- **HTML отчёт** со статистикой за 24 часа

## Структура проекта 
[200~server-monitor/
├── config/config.yaml       — пороги и пути
├── scripts/
│   ├── monitor.sh           — запуск мониторинга (cron)
│   └── backup.sh            — запуск бэкапа (cron)
├── python/
│   ├── collector.py         — сбор метрик
│   ├── alerter.py           — проверка порогов
│   ├── backup_manager.py    — создание и ротация бэкапов
│   └── report_generator.py  — генерация HTML отчёта
├── logs/                    — все логи и метрики
├── crontab.example          — пример настройки cron
└── install.sh               — установка~

## Установка

```bash
git clone https://github.com/ВАШ_НИК/server-monitor.git
cd server-monitor
bash install.sh
```

## Ручной запуск

```bash
# Мониторинг
bash scripts/monitor.sh

# Бэкап
bash scripts/backup.sh

# HTML отчёт
python3 python/report_generator.py
# Открыть: logs/report.html
```

## Настройка порогов

Редактируй `config/config.yaml`:

```yaml
thresholds:
  cpu_percent: 80      # алерт если CPU выше
  disk_percent_free: 15 # алерт если диск свободен меньше
  ram_percent: 90      # алерт если RAM выше
```

## Cron

```bash
crontab -e
# вставить содержимое crontab.example
```
