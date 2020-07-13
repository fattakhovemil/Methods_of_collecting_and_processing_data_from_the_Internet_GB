import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from pymongo import errors
from selenium.webdriver.chrome.options import Options


def save_data_to_db(data):
    try:
        data_base.goods.replace_one(data, data, upsert=True)
    except errors.DuplicateKeyError:
        pass
        return 0
    else:
        return 1


client = MongoClient('localhost', 27017)
data_base = client['db_goods']
chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome('./chromedriver.exe', options=chrome_options)
driver.get("https://www.mvideo.ru")
items_list = []
items_count = 0
while True:
    name = driver.find_element_by_class_name('sel-product-tile-title').text
    link = driver.find_element_by_class_name('sel-product-tile-title').get_attribute('href')
    price = driver.find_element_by_class_name('c-pdp-price__current').text
    for i in range(4):
        top_hit = {"name": name[i], "link": link[i], "price": price[i]}
        items_list.append(top_hit)
        items_count += save_data_to_db(top_hit)
    try:
        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Хиты "
                                                                                           "продаж')]/ancestor::div["
                                                                                           "@class='section']//a["
                                                                                           "@class='next-btn "
                                                                                           "sel-hits-button-next']")))
        button.click()
        time.sleep(2)
    except:
        break

print(f'Просмотрено товаров: {items_count}')
