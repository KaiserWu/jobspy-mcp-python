FROM python:3.11-slim
ARG PIP_INDEX_URL=https://pypi.org/simple/
ARG PIP_EXTRA_INDEX_URL=""
ENV TRANSPORTER="http"
WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && \
	pip install -r requirements.txt

COPY main.py /app
COPY jobspy_mcp.py /app
COPY __init__.py /app

EXPOSE 5566

CMD ["/bin/sh", "-c", "python main.py -t ${TRANSPORTER}"]
