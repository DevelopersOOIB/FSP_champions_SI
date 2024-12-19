FROM python:3.9-slim
COPY app.py /app/app.py
COPY templates /app/templates
COPY static /app/static 
WORKDIR /app
RUN pip install --no-cache-dir flask
ARG FLAG="flag{ssti_explo1t3d_succ3ssfully}"
RUN echo $FLAG > /app/flag.txt
CMD ["python", "app.py"]]

