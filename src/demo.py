from Key import *
import tweepy
from bot import *
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import logging
import threading

#from requests_oauthlib import OAuth1Session
Twitter_ID = "eigoyurusan"
SCREEN_NAME = 'eigoyurusan'

def auto_reply(bot, lock,driver):
    logging.debug('function of auto reply start')
    while True:
        bot.reply(lock,driver)
        time.sleep(600)

def auto_tweets(bot,lock,driver):
    logging.debug('function of auto tweets start')
    while True:
        bot.auto_tweet(lock,driver)
        time.sleep(1000)



if __name__ == '__main__':
    #ツイッターapiの作成
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)
    bot = EigoyurusanBot(api,Twitter_ID,SCREEN_NAME)

    now_path = os.path.dirname(os.path.abspath(__file__))
    driver_path = now_path + '/google-chrome'
    #翻訳用ドライバーをheadless modeで開く
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(driver_path, options=options)
    lock = threading.Lock()
    #リプライ要のスレッド
    auto_reply_thread = threading.Thread(target=auto_reply, args=(bot,lock,driver))
    #自動ツイート用のスレッド
    auto_tweet_thread = threading.Thread(target=auto_tweets, args=(bot,lock,driver))
    auto_reply_thread.start()
    auto_tweet_thread.start()

    # 翻訳用ドライバー閉じる
    driver.close()
