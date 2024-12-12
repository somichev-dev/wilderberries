from bs4 import BeautifulSoup
import json, time
from DrissionPage import ChromiumPage, ChromiumOptions
import random

MAX_PRODUCT_ID = 300000000
MIN_PRODUCT_ID = 100000001
BASELINK = "https://www.wildberries.ru/catalog/"

def get_random_id() -> int:
    return random.randint(MIN_PRODUCT_ID, MAX_PRODUCT_ID)

class Product():
    _product_id = 0
    _html_raw = ""
    _soup = ""
    product_link = ""
    name = ""
    rating = 1
    rating_amount = ""
    cost = 1
    thumbnail_link = ""

    def __init__(self, product_id = 0):
        self._product_id = str(product_id)
        self.product_link = BASELINK + self._product_id + "/detail.aspx"
        self._html_raw = self._get_raw_html()
        self._soup = self._get_soup()
        self._parse_soup()

    def _parse_soup(self):
        ## Проверка на существование страницы
        if(len(self._soup.select(".content404__title")) > 0):
            raise ProductNotFoundException
        if(len(self._soup.select(".content500:__title")) > 0):
            raise ProductNotFoundException
        if(len(self._soup.select(".product-page__title")) == 0):
            raise ProductNotFoundException
        self.name = self._soup.select(".product-page__title")[0].text
        ## Проверка на наличие рейтингов у товара
        if("Нет оценок" in self._soup.select(".product-review__rating")[0].text):
            self.rating = "?"
            self.rating_amount = "Нет оценок"
        else:
            self.rating = self._soup.select(".product-review__rating")[0].text
            self.rating_amount = self._soup.select(".product-review__count-review")[0].text
            self.rating_amount = self.rating_amount.replace("\xa0", "")
        ## Проверка ан наличие товара (и цены соответственно)
        if(len(self._soup.select("div.product-page__price-block-wrap:nth-child(3) > p:nth-child(4) > span:nth-child(3)")) > 0):
            self.cost = "Нет в наличии"
        else:
            self.cost = self._soup.select(".price-block__final-price")[0].text
            self.cost = self.cost.replace("\xa0", " ")
        ## Парсим изображение для превью
        self.thumbnail_link = self._soup.select("li.swiper-slide:nth-child(2) > div:nth-child(3) > img:nth-child(2)")
        if(len(self.thumbnail_link) > 0):
            self.thumbanil_link = self.thumbnail_link[0]["src"]
            self.thumbnail_link = self.thumbanil_link.replace("big", "c246x328")
        else:
            self.thumbnail_link = self._soup.select("li.swiper-slide:nth-child(1) > div:nth-child(3) > img:nth-child(2)")
            if(len(self.thumbnail_link) > 0):
                self.thumbanil_link = self.thumbnail_link[0]["src"]
                self.thumbnail_link = self.thumbanil_link.replace("big", "c246x328")
            else:
                self.thumbnail_link = "https://somichev.dev/mug/green.png"
        pass

    def _request_product(self) -> ChromiumPage:
        options = ChromiumOptions()
        options.set_user_agent(
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        options.headless()
        options.set_argument('--no-sandbox')
        options.set_argument('--headless=new')
        page = ChromiumPage(options)
        page.get(self.product_link)
        time.sleep(3)
        return page

    def _get_raw_html(self):
        product_response = self._request_product()
        return product_response.html

    def _get_soup(self):
        soup = BeautifulSoup(self._html_raw, 'html.parser')
        return soup

class CaptchaException(Exception):
    pass

class ProductNotFoundException(Exception):
    pass

if __name__ == "__main__":
    Product(241959443)