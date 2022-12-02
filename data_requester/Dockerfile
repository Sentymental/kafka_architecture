FROM python:3.10

WORKDIR /app

RUN apt-get update
RUN apt install -y \
    gcc g++ python-dev librocksdb-dev build-essential \
    libsnappy-dev zlib1g-dev libbz2-dev libgflags-dev \
    liblz4-dev libzstd-dev curl

COPY ./app /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn main:app --reload --host 0.0.0.0 --port 8009