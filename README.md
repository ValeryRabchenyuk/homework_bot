# Бот-ассистент

### Описание проекта

Telegram-бот, который раз в 10 минут обращается к API сервиса Практикум.Домашка и узнаёт статус домашней работы: взята ли в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

### Стек технологий
<div>
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
</div>

### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:
```
git clone <project_url>
```
```
cd homework_bot
```

Создать и активировать виртуальную среду:
```
python -m venv venv
```
```
source venv/Scripts/activate
```

Установить зависимости из файла `requirements.txt`:
```
pip install -r requirements.txt
```

Запустить файл `homework.py`:
```
python homework.py
```
