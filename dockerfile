FROM python:3.6-alpine

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT 8080

CMD [ "python", "app.py" ]
