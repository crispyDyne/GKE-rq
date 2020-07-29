FROM python:3

COPY ./src/. /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT 6379

CMD [ "rq", "worker","--url", "redis://10.116.18.83:6379", "rq-server" ]
