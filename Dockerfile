FROM python:3.12-alpine

# Устанавливаем необходимые пакеты
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Копируем все файлы проекта
COPY . .

WORKDIR .

# Запуск контейнера
CMD ["python", "main.py"]
