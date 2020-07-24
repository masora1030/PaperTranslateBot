from Key import *
import tweepy
from bot import *
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions as Options

if __name__ == '__main__':
    #ツイッターapiの作成
    now_path = os.path.dirname(os.path.abspath(__file__))
    driver_path = now_path + '/google-chrome'
    #翻訳用ドライバーをheadless modeで開く
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=options)
    driver.close()
