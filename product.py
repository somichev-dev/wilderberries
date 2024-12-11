from bs4 import BeautifulSoup
import json
from DrissionPage import ChromiumPage, ChromiumOptions

MAX_PRODUCT_ID = 1635813225
BASELINK = "https://www.ozon.ru/product/"

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
        self.product_link = BASELINK + self._product_id + "/?oos_search=false"
        self._html_raw = self._get_raw_html()
        self._soup = self._get_soup()
        self._parse_soup()

    def _parse_soup(self):
        ratings = []
        try:
            self.name = self._soup.select(".tm6_27")[0].text
        except IndexError:
            raise ProductNotFoundException()
        try:
            ratings = self._soup.select(".zu9_30 > div:nth-child(2)")[0].text.rstrip().split('•')
        except IndexError:
            ratings = [" ?", " Нет отзывов"]
        
        self.rating = str(ratings[0])
        if(len(ratings) != 1):
            self.rating_amount = ratings[1]
        else:
            self.rating = "?"
            self.rating_amount = " Нет отзывов"
        self.cost = self._soup.select(".mt0_27")[0].text
        try:
            self.thumbnail_link = self._soup.select(".qk6_27")[0]["src"]
        except IndexError:
            self.thumbnail.lint = "https://somichev.dev/mug/green.png"
        self.cost = self.cost.replace(u'\u2009', '')
        self.rating = self.rating.replace(" ", "")
        self.rating_amount = self.rating_amount.replace(" ", "", 1)
        self.name = self.name.replace('\n', "")

    def _request_product(self) -> ChromiumPage:
        options = ChromiumOptions()
        options.set_user_agent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
        options.headless()
        options.set_argument('--no-sandbox')
        options.set_argument('--headless=new')

        page = ChromiumPage(options)
        page.get(self.product_link)

        page.get_screenshot("image.png")
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
    Product(1632047221)