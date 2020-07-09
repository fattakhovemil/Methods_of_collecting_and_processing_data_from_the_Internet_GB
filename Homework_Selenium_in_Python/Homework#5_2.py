import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient


def mvideo_site():
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get("https://www.mvideo.ru")
    # assert "Сайт техники MVideo" in driver.title
    headers = driver.find_elements_by_class_name("indexGoods__headers")
    for i in range(0, len(headers)):
        if headers[i].text == "Хиты продаж":
            header_hit = headers[i]
    top_hit = header_hit.find_element_by_xpath("..")

    item = top_hit.find_elements_by_class_name("indexGoods__item")

    client = MongoClient('localhost', 27017)
    data_base = client['db_goods']
    top_hits = data_base.hits

    for i in range(0, len(item), 2):
        name = item[i].find_element_by_class_name("indexGoods__item__descriptionCover").find_element_by_tag_name(
            "a").get_attribute("title").replace("Подробнее о «", "").replace("»", "")
        link = item[i].find_element_by_class_name("indexGoods__item__descriptionCover").find_element_by_tag_name(
            "a").get_attribute("href")
        price = item[i].find_element_by_class_name("indexGoods__item__price").text
        print(name, link, price)
        top_hit = {"name": name,
                   "link": link,
                   "price": price}
        top_hits.insert_one(top_hit)


mvideo_site()
