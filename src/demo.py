from Key import *
import tweepy
from bot import *
import time

import logging
import threading

#from requests_oauthlib import OAuth1Session
Twitter_ID = "eigoyurusan"
SCREEN_NAME = 'eigoyurusan'

def auto_reply(bot, lock):
    logging.debug('function of auto reply start')
    while True:
        bot.reply(lock)
        time.sleep(60)

def auto_tweets(bot,lock):
    logging.debug('function of auto tweets start')
    while True:
        bot.reply(lock)
        time.sleep(600)



if __name__ == '__main__':
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)
    bot = EigoyurusanBot(api,Twitter_ID,SCREEN_NAME)#bot オブジェクト

    lock = threading.Lock()
    auto_reply_thread = threading.Thread(target=auto_reply, args=(bot, lock))
    auto_tweet_thread = threading.Thread(target=auto_tweets, args=(bot, lock))
    auto_reply_thread.start()
    auto_tweet_thread.start()
