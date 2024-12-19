FROM python:3.9-slim
RUN pip install flask
COPY main.py /app/main.py
COPY templates /app/templates
WORKDIR /app
ARG FLAG="flag{pyth0_expl0it_inj3ct10n}"
RUN echo $FLAG > /app/flag.txt
EXPOSE 5000
CMD ["python", "main.py"]

