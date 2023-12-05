import re

from bs4 import BeautifulSoup
import urllib3

from price_tracker.user_agent import session

urllib3.disable_warnings()


def request_sender(url, ssl_verification_bypass=False):
    if ssl_verification_bypass:
        page = session.get(url, verify=False)
    else:
        page = session.get(url)
    return BeautifulSoup(page.content, 'html.parser')


class Scraper:
    def __init__(self, mailer):
        self.mailer = mailer

    def mail_decider(self, url, product_name, price, warn_price):
        if price < warn_price:
            self.mailer.send_mail(url, product_name, price)
            return True
        return False

    def check_hepsiburada_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find(class_='product-name').get_text()
        price = float(soup.select_one('span[itemprop=price]')['content'])

        return self.mail_decider(url, product_name, price, warn_price)

    def check_gittigidiyor_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find(id='sp-title').get_text().strip()
        price = float(
            re.findall(r'\d+\.\d+', soup.find(class_='lastPrice').get_text().replace('.', '').replace(',', '.'))[0]
        )

        return self.mail_decider(url, product_name, price, warn_price)

    def check_trendyol_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find('title').get_text().split(' | ')[0]
        price = soup.find(class_='prc-dsc')
        if not price:
            price = soup.find(class_='prc-slg')

        price = float(
            re.findall(r'\d+\.\d+', price.get_text().replace(',', '.'))[0]
        )

        return self.mail_decider(url, product_name, price, warn_price)

    def check_amazon_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find(id='productTitle').get_text().strip()

        price = soup.find(id='priceblock_dealprice')
        if not price:
            price = soup.find(id='priceblock_ourprice')

        price = float(
            re.findall(r'\d+\.\d+', price.get_text().replace('.', '').replace(',', '.'))[0]
        )

        return self.mail_decider(url, product_name, price, warn_price)

    def check_vatan_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find(class_='product-list__product-name').get_text().strip()

        price = float(soup.find(class_='product-list__price').get_text())

        return self.mail_decider(url, product_name, price, warn_price)

    def check_teknosa_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url, True)

        product_name = soup.find(class_='product-title').get_text().strip()

        price = float(soup.find(id='addToCartButton')['data-product-price'])

        return self.mail_decider(url, product_name, price, warn_price)

    def check_n11_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find(class_='proName').get_text().strip()

        price = float(
            re.findall(r'"lowPrice": "(.*)"', soup.prettify())[0]
        )

        return self.mail_decider(url, product_name, price, warn_price)

    def check_ciceksepeti_net_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find(class_='o-productDetail__title').get_text().strip()

        price = float(
            re.findall(r'\d+\.\d+',
                       soup.find(class_='m-productPrice__salePrice').get_text().replace('\n', '').replace(',', '.'))[0]
        )

        return self.mail_decider(url, product_name, price, warn_price)

    def check_ciceksepeti_com_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find(class_='product__info__title').get_text().strip()

        price = soup.find(class_='product__info__new-price__integer').get_text() + soup.find(
            class_='product__info__new-price__decimal').get_text().replace(',', '.')
        price = float(re.findall(r'\d+.\d+', price)[0])

        return self.mail_decider(url, product_name, price, warn_price)

    def check_mediamarkt_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find('title').get_text().strip()

        price = float(soup.select_one('meta[itemprop=price]')['content'])

        return self.mail_decider(url, product_name, price, warn_price)

    def check_ebay_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.select_one('h1', id='itemTitle')
        [x.extract() for x in product_name.findAll('span')]
        product_name = product_name.get_text().strip()

        price = float(
            re.findall(r'\d+\.\d+', soup.find(id='prcIsum').get_text())[0]
        )

        return self.mail_decider(url, product_name, price, warn_price)

    def check_morhipo_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find('title').get_text().strip().split(' | ')[0]

        price = soup.select_one('span.badge-price')
        if not price:
            price = soup.select_one('span.final-price')
        price = float(re.findall(r'\d+\.\d+', price.get_text().replace(',', '.'))[0])

        return self.mail_decider(url, product_name, price, warn_price)

    def check_teknostore_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find(class_='page-title').get_text().strip()

        price = float(soup.select_one('span[data-price-type=finalPrice]')['data-price-amount'])

        return self.mail_decider(url, product_name, price, warn_price)

    def check_letgo_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.select_one('div[data-test=name]').get_text()

        price = float(
            re.findall(r'\d+.\d+', soup.find(class_='price').get_text().replace('.', ''))[0]
        )

        return self.mail_decider(url, product_name, price, warn_price)

    def check_kitapyurdu_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find(class_='pr_header__heading').get_text()

        price = float(
            re.findall(r'\d+\.\d+', soup.find(class_='price__item').get_text().replace(',', '.'))[0]
        )

        return self.mail_decider(url, product_name, price, warn_price)

    def check_tozlu_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find('title').get_text().strip()

        price = float(
            re.findall(r'\d+\.\d+', soup.find(class_='spanFiyat').get_text().replace(',', '.'))[0]
        )

        return self.mail_decider(url, product_name, price, warn_price)

    def check_dandr_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find(class_='product-name').get_text().strip()

        price = float(
            re.findall(r'\d+,\d+', soup.find(class_='product-price').get_text())[0].replace(',', '.')
        )

        return self.mail_decider(url, product_name, price, warn_price)

    def check_toyzzshop_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find(id='metaTitle').get_text()

        price = float(
            re.findall(r'\d+\.\d+', soup.find(class_='fs-40').get_text().replace(',', '.'))[0]
        )

        return self.mail_decider(url, product_name, price, warn_price)

    def check_decathlon_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find(id='productName').get_text()

        price = float(soup.find(id='real_price')['data-price'])

        return self.mail_decider(url, product_name, price, warn_price)

    def check_nike_product(self, url: str, warn_price: float) -> bool:
        soup = request_sender(url)

        product_name = soup.find('title').get_text().split('. ')[0]

        price = soup.select_one('div[data-test=product-price-reduced]')
        if not price:
            price = soup.select_one('div[data-test=product-price]')
        price = float(
            re.findall(r'\d+\.\d+', price.get_text().replace('.', '').replace(',', '.'))[0]
        )

        return self.mail_decider(url, product_name, price, warn_price)
