@echo off

call %~dp0venv\Scripts\activate

cd %~dp0IT_ANALYTICS\

pip install django
pip install Pillow
pip install requests

python manage.py runserver

pause