#!/bin/bash
echo "Создание виртуального окружения..."
python3 -m venv venv

echo "Активация виртуального окружения..."
source venv/bin/activate

echo "Обновление pip..."
python -m pip install --upgrade pip

echo "Установка зависимостей..."
pip install -r requirements.txt

echo "Настройка завершена!"
echo "Для активации окружения используйте: source venv/bin/activate" 