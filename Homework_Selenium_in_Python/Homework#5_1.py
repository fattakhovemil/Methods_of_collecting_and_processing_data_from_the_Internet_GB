import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def mail_site():
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    driver = webdriver.Chrome('./chromedriver.exe', options=chrome_options)
    driver.get('https://mail.ru')
    login = driver.find_element_by_id('mailbox:login')
    login.send_keys('study.ai_172@mail.ru')
    login.send_keys(Keys.ENTER)
    time.sleep(0.9)
    password = driver.find_element_by_id('mailbox:password')
    password.send_keys('NextPassword172')
    password.send_keys(Keys.ENTER)
    time.sleep(8)
    mail_links = set()
    last_block = None
    while True:
        time.sleep(7)
        block = driver.find_elements_by_class_name('js-letter-list-item')
        for value in block:
            mail_links.add(value.get_attribute('href'))
        if block[-1] != last_block:
            last_block = block[-1]
            actions = ActionChains(driver)
            actions.move_to_element(last_block)
            actions.perform()
        else:
            break
    letters_all = []
    for link in mail_links:
        driver.get(link)
        time.sleep(3)
        letter_topic = driver.find_element_by_class_name('thread__subject').text
        letter_date = driver.find_element_by_class_name('letter__date').text
        letter_content = driver.find_element_by_class_name('letter-body').text
        letters_all.append({'date': letter_date,
                            'topic': letter_topic,
                            'content': letter_content})
        driver.get('https://e.mail.ru/inbox/')
        time.sleep(3)
    driver.quit()
    print(len(letters_all))


mail_site()