FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy new relic config (This will be stored and copied from some storage like s3)
COPY newrelic.ini /app/newrelic.ini

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py wait_for_db && python manage.py migrate && newrelic-admin run-program python manage.py runserver 0.0.0.0:8000"]
