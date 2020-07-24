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

def auto_reply(bot):
    logging.debug('function of auto reply start')
    while True:
        bot.reply()
        time.sleep(600)

def auto_tweets(bot):
    logging.debug('function of auto tweets start')
    while True:
        bot.auto_tweet()
        time.sleep(1000)



if __name__ == '__main__':
    #ツイッターapiの作成
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)


    now_path = os.path.dirname(os.path.abspath(__file__))
    driver_path = now_path + '/google-chrome'
    #翻訳用ドライバーをheadless modeで開く
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(driver_path, options=options)
    lock = threading.Lock()

    bot = EigoyurusanBot(api,Twitter_ID,SCREEN_NAME,driver,lock)

    #リプライ要のスレッド
    auto_reply_thread = threading.Thread(target=auto_reply, args=(bot))
    #自動ツイート用のスレッド
    auto_tweet_thread = threading.Thread(target=auto_tweets, args=(bot))
    auto_reply_thread.start()
    auto_tweet_thread.start()
