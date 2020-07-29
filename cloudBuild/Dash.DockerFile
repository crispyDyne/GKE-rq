FROM python:3

COPY ./src/. /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT 9181

CMD [ "rq-dashboard","-u", "redis://10.116.18.83:6379"]
