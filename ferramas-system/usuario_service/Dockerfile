FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
  && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir whitenoise==6.5.0

COPY . .

# Ya no corremos migrate en build
# RUN python manage.py migrate --noinput
# RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["uvicorn", "usuario_service.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
