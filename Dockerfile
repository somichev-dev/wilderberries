FROM python:3.12.8-alpine

WORKDIR /root

COPY requirements.txt .

RUN apk add gcc python3-dev musl-dev linux-headers
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
COPY product.py .
COPY token .
COPY flavors.txt .

RUN apk add chromium

CMD ["sh"]