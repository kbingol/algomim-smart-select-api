FROM python:3.11.4

RUN pip install python-dotenv==1.0.0 firebase_admin==6.2.0 Flask==2.3.2 gunicorn==21.2.0 Flask_Cors==4.0.0

COPY src/ app/

WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app