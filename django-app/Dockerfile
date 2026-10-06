FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN dos2unix entrypoint.sh && chmod +x entrypoint.sh

EXPOSE 8000

ENV PORT=8000
ENV DJANGO_SETTINGS_MODULE=dealership_project.settings
ENV EXPRESS_SERVICE_URL=http://express-service:3030
ENV SENTIMENT_SERVICE_URL=http://sentiment-service:5000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "dealership_project.wsgi:application"]
