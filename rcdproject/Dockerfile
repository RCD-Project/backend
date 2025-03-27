FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD python manage.py migrate && exec gunicorn -b :$PORT rcdproject.wsgi

