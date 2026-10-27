#!/usr/bin/env bash
# Выход при ошибке
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Сбор статики (CSS, картинки)
python manage.py collectstatic --no-input

# Применение миграций к базе
python manage.py migrate
