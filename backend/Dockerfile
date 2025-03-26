FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt /app/
RUN apk add --no-cache gcc musl-dev libffi-dev python3-dev postgresql-dev
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x run.sh

CMD ["/app/run.sh"]
