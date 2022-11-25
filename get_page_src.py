import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random
from dotenv import load_dotenv, find_dotenv

urls = ['https://www.facebook.com/groups/search/groups?q=asic%20mining',
        'https://www.facebook.com/groups/search/groups?q=crypto%20mining']


class ColectData:
    def __init__(self, driver: webdriver):
        self.driver = driver
        card_mask = '//div[@class="x9f619 x1n2onr6 x1ja2u2z x2bj2ny x1qpq9i9 xdney7k ' \
                    'xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld"]'
        facebook_url_mask = '//a[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk ' \
                            'xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd ' \
                            'x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f"]'
        self.card_item = driver.find_elements(By.XPATH, card_mask)
        self.facebook_url = driver.find_elements(By.XPATH, facebook_url_mask)

    def get_card_data(self):
        facebook_info = []
        for num, card in enumerate(self.card_item):
            facebook_info.append({
                'card_data': card.text,
                'facebook_url': self.facebook_url[num].get_attribute('href')
            })
        return facebook_info


def scroll_page(driver: webdriver):
    print('[INFO] Scrolling target page ...')
    last_height = None
    while True:
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
        driver.execute_script(f"window.scrollTo(0, {new_height})")
        time.sleep(random.randint(1, 2))
        last_height = new_height


def get_groups_data(driver: webdriver, file_name: str):
    driver.get(urls[0])
    time.sleep(random.randint(2, 4))
    scroll_page(driver)
    collect_data = ColectData(driver=driver)
    card_data = collect_data.get_card_data()
    with open(f'json/{file_name}.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(card_data))
        print('[INFO] Save file to json')


def init_driver() -> webdriver:
    s = Service('C:/PyProject/chromedriver.exe')
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })
    browser = webdriver.Chrome(service=s, options=chrome_options)
    return browser


def login(driver: webdriver):
    url = 'https://www.facebook.com/'
    driver.get(url)
    time.sleep(random.randint(2, 3))
    load_dotenv(find_dotenv())
    linkedin_login = os.getenv('LOGIN')
    linkedin_password = os.getenv('PASS')
    driver.find_element(By.XPATH, '//input[@name="email"]').send_keys(linkedin_login)
    driver.find_element(By.XPATH, '//input[@name="pass"]').send_keys(linkedin_password)
    driver.find_element(By.XPATH, '//button[@name="login"]').click()
    time.sleep(random.randint(2, 4))


def get_webpage_data():
    driver = init_driver()
    login(driver)
    get_groups_data(driver, 'asic_mining')
    driver.close()
    driver.quit()
