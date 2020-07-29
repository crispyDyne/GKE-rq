FROM python:3

COPY ./src/. /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT 8080

CMD [ "python", "app.py" ]
