@echo off
echo Создание виртуального окружения...
python -m venv venv

echo Активация виртуального окружения...
call venv\Scripts\activate

echo Обновление pip...
python -m pip install --upgrade pip

echo Установка зависимостей...
pip install -r requirements.txt

echo Настройка завершена!
echo Для активации окружения используйте: venv\Scripts\activate
pause 