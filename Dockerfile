FROM python:3.12.8-alpine

WORKDIR /root

COPY requirements.txt .

RUN apk add gcc python3-dev musl-dev linux-headers
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
COPY product.py .
COPY token .

RUN apk add chromium

RUN touch crontab.tmp \
    && echo "30 7 * * * python ./bot.py" > crontab.tmp \
    && crontab crontab.tmp \
    && rm -rf crontab.tmp

CMD ["/usr/sbin/crond", "-f", "-d", "0"]
