FROM python:3.9-slim
RUN apt-get update && apt-get install -y iputils-ping

COPY app.py /app/app.py
COPY templates /app/templates
COPY templates /app/.hidden/
WORKDIR /app

RUN pip install flask

CMD ["python", "app.py"]
