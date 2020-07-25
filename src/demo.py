from Key import *
import tweepy
from bot import *
import time, datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import logging
import threading

#from requests_oauthlib import OAuth1Session
Twitter_ID = "eigoyurusan"
SCREEN_NAME = 'eigoyurusan'

def auto_reply(bot, interval, initsleep=None):
    logging.debug('function of auto reply start')
    if initsleep==None:
        now = datetime.datetime.now()
        initsleep = interval-(now.minute*60+now.second+now.microsecond/100000)%interval
    print(f'[auto reply] initial sleep: {initsleep} s')
    time.sleep(initsleep)
    print(f"[auto reply] started at {datetime.datetime.now()}")
    while True:
        bot.reply()
        time.sleep(interval)

def auto_tweets(bot, interval, initsleep=None):
    logging.debug('function of auto tweets start')
    if initsleep==None:
        now = datetime.datetime.now()
        initsleep = interval-(now.minute*60+now.second+now.microsecond/100000)%interval
    print(f'[auto tweet] initial sleep: {initsleep} s')
    time.sleep(initsleep)
    print(f"[auto tweet] started at {datetime.datetime.now()}")
    while True:
        bot.auto_tweet()
        time.sleep(interval)



if __name__ == '__main__':
    #ツイッターapiの作成
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)

    lock = threading.Lock()

    bot = EigoyurusanBot(api,Twitter_ID,SCREEN_NAME,lock)
    
    #リプライ要のスレッド
    auto_reply_thread = threading.Thread(target=auto_reply, args=(bot,10*60,0))
    #自動ツイート用のスレッド
    auto_tweet_thread = threading.Thread(target=auto_tweets, args=(bot,60*60,0))
    
    auto_reply_thread.start()
    auto_tweet_thread.start()
