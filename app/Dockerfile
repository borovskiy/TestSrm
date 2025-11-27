FROM python:3.11-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Устанавливаем зависимости
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем весь код в /app/app (ВЛОЖЕННО!)
COPY ./app /app/app
