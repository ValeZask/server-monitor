# 🖥️ Server Monitor

Система мониторинга сервера с алертами, автоматическими бэкапами и HTML-отчётами.

## Что делает

- **Мониторинг** CPU, RAM и диска каждые 5 минут
- **Алерты** в `logs/alerts.log` при превышении порогов
- **Автоматический бэкап** папок в `.tar.gz` каждую ночь в 02:00
- **Ротация** — хранит только 7 последних бэкапов
- **HTML-отчёт** со статистикой за последние 24 часа

## Структура проекта

```text
server-monitor/
├── config/config.yaml       # пороги и пути
├── scripts/
│   ├── monitor.sh           # запуск мониторинга (cron)
│   └── backup.sh            # запуск бэкапа (cron)
├── python/
│   ├── collector.py         # сбор метрик
│   ├── alerter.py           # проверка порогов
│   ├── backup_manager.py    # создание и ротация бэкапов
│   └── report_generator.py  # генерация HTML-отчёта
├── logs/                    # логи и метрики
├── crontab.example          # пример настройки cron
└── install.sh               # установка
```

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

# HTML-отчёт
python3 python/report_generator.py

# Открыть отчёт
logs/report.html
```

## Настройка порогов

Отредактируйте файл `config/config.yaml`:

```yaml
thresholds:
  cpu_percent: 80        # алерт, если CPU выше 80%
  disk_percent_free: 15  # алерт, если свободно менее 15%
  ram_percent: 90        # алерт, если RAM выше 90%
```

## Cron

```bash
crontab -e
# вставьте содержимое файла crontab.example
```

## Что я изучил

### Linux

- Навигация по файловой системе и права доступа (`chmod`, `ls -la`)
- Работа с процессами и системными файлами
- Переменные окружения и пути

### Bash

- Написание скриптов автоматизации
- Использование `tee`, `cat`, `mkdir`, `touch`
- Перенаправление вывода
- Heredoc-синтаксис (`<< 'EOF'`)

### Python

- Сбор системных метрик через `psutil`
- Работа с JSON и YAML
- Генерация HTML-отчётов

### Git

- Базовый workflow: `add` → `commit` → `push`
- Создание тегов (`git tag v1.0.0`)
- Работа с GitHub через CLI (`gh`)

### Cron

- Формат записей crontab
- Планирование задач по расписанию
- Логирование вывода cron-задач

### DevOps-принципы

- Структура проекта и документация
- Конфигурация через отдельный файл (`config.yaml`)
- Разделение ответственности: сбор → анализ → отчёт
