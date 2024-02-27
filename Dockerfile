# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.9
# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /app
# Скачиваем/обновляем необходимые библиотеки для проекта 
COPY requirements.txt /app
RUN pip3 install --upgrade pip -r requirements.txt
# |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile, 
# в рабочую директорию контейнера
COPY . /app
# Устанавливаем порт, который будет использоваться для сервера
EXPOSE 7000

RUN cd app

CMD uvicorn main:app --host 0.0.0.0 --port 7000  --root-path /chrome_ext