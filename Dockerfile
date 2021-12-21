FROM python:3.8

COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential libpoppler-cpp-dev pkg-config python-dev
RUN pip install --no-cache-dir -r requirements.txt

ADD src .
COPY data data

CMD [ "python", "./main.py" ]
