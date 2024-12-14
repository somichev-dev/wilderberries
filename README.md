# wilderberries
Бот для нахождения и отправки случайных товаров с маркетплейсов. В репозитории версия для поиска товаров [Wildberries](https://www.wildberries.ru/).

# Зачем это нужно?
Не могу сказать.

# Установка
## Dockerfile
```bash
git clone https://github.com/somichev-dev/wilderberries.git
cd wilderberries
docker build -t wilderberries-app .
docker run wilderberries-app
```
## Установка напрямую
```bash
git clone https://github.com/somichev-dev/wilderberries.git
cd wilderberries
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ./bot.py
```
