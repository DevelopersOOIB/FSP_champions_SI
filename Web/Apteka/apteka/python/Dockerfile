FROM python:3.8

WORKDIR /app

COPY ./ .

RUN pip install Flask
RUN pip install psycopg2-binary

CMD ["python", "app.py"]
