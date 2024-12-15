FROM python:3.12.8-alpine

WORKDIR /root

COPY requirements.txt .
COPY bot.py .
COPY product.py .
COPY flavors.txt .
COPY config.toml .

RUN apk add gcc python3-dev musl-dev linux-headers chromium
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./bot.py"]
