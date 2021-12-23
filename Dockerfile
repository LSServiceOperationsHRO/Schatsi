FROM python:3.9-slim-bullseye

COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config && \
    apt-get clean
RUN pip install --no-cache-dir -r requirements.txt

ADD src .
COPY data data

COPY .aws /root/.aws

CMD [ "python", "./main.py" ]
