import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver():
    now_path = os.path.dirname(os.path.abspath(__file__))
    driver_path = now_path + '/chromedriver'

    # 翻訳用ドライバーをheadless modeで開く
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(driver_path, options=options)

    return driver
