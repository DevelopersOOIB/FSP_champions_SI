FROM python:3.8

WORKDIR /app

COPY ./ .
COPY ./flag.txt /etc/flag.txt

RUN pip install psycopg2-binary
RUN pip install Flask
RUN pip install lxml

CMD ["python", "app.py"]
