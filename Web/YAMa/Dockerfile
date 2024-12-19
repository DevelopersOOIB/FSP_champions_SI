FROM python:3.9-slim
RUN pip install flask pyyaml
WORKDIR /app
COPY app.py /app/
COPY templates /app/templates
ARG FLAG="flag{fl4g_h1dd3n_1n_js0n}"
RUN echo $FLAG > /app/flag.txt
CMD ["python", "app.py"]
