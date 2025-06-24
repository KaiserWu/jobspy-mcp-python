FROM python:3.11-slim

ENV TRANSPORTER="http"
WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "main.py", "-t", "${TRANSPORTER}"]