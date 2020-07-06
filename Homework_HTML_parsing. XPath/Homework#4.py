from pprint import pprint
from lxml import html
import requests
from datetime import date
from pymongo import MongoClient

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

def request_to_yandex():
    response = requests.get('https://yandex.ru', headers=header)
    dom = html.fromstring(response.text)

    list = []
    items = dom.xpath("//ol/li[contains(@class,'list__item  list__item_icon')]")
    for item in items:
        news = {}
        source = item.xpath(".//object[@class='news__agency-icon-image']/@title")
        news_title = item.xpath(".//a/@aria-label")
        link = item.xpath(".//a/@href")
        date_of_publication = date.today().isoformat()

        news['source'] = source[0]
        news['news'] = news_title[0]
        news['link'] = link[0]
        news['date'] = date_of_publication

        list.append(news)
    return(list)


def request_to_mail():
    response = requests.get('https://news.mail.ru/', headers=header)
    dom = html.fromstring(response.text)

    list = []
    items = dom.xpath("//ul[@class='list list_type_square list_half js-module']//li[@class='list__item']")
    for item in items:
        news = {}
        news_title = item.xpath(".//a[@class='list__text']/text()")
        link = item.xpath(".//a[@class='list__text']/@href")
        date_of_publication = date.today().isoformat()

        news_title[0] = news_title[0].replace('\xa0', ' ')
        link = str(link[0])
        common_link = 'https://news.mail.ru/' + link

        response_page = requests.get(common_link, headers=header)
        dom_page = html.fromstring(response_page.text)
        items_page = dom_page.xpath("//div[@class='breadcrumbs breadcrumbs_article js-ago-wrapper']//span[@class='breadcrumbs__item']//span[@class='note']")

        for value in items_page:
            source = value.xpath(".//a[@class='link color_gray breadcrumbs__link']//span[@class='link color_gray breadcrumbs__link']/text()")

        news['source'] = source
        news['news'] = news_title[0]
        news['link'] = link
        news['date'] = date_of_publication
        list.append(news)
    return (list)


def request_to_lenta():
    response = requests.get('https://lenta.ru/', headers=header)
    dom = html.fromstring(response.text)

    list = []
    items = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']")
    for item in items:
        new = {}
        news_title = item.xpath(".//div[@class='item']//a/text() | .//div[@class='first-item']//h2//a/text()")
        link = item.xpath(".//div[@class='item']//a/@href | .//div[@class='first-item']//h2//a/@href")
        date_of_publication = item.xpath(".//div[@class='item']//a/time/@datetime | .//div[@class='first-item']//h2//a/time/@datetime")

        new['source'] = 'lenta.ru'
        new['news'] = news_title
        new['link'] = link
        new['date'] = date_of_publication
        list.append(new)
    return (list)

#pprint(request_to_yandex())
#pprint(request_to_mail())
#pprint(request_to_mail())

client = MongoClient('localhost', 27017)
db = client['news_db']

news_collection = db.news_collection

to_insert = [request_to_yandex(), request_to_mail(), request_to_lenta()]
for collection in to_insert:
    news_collection.insert_many(collection)