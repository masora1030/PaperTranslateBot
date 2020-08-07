from bot import *
import sys, time, datetime, threading
from logging import basicConfig, getLogger, INFO

basicConfig(level=INFO)
logger = getLogger('_')

def interval_sleep(interval, initsleep, funcname):
    if initsleep==None:
        now = datetime.datetime.now()
        initsleep = interval-(now.minute*60+now.second+now.microsecond/100000)%interval
    logger.debug(f'[{funcname}] sleep: {initsleep} s')
    time.sleep(initsleep)
    logger.info(f"[{funcname}] started at {datetime.datetime.now()}")

def run(func, interval, initsleep, funcname):
    interval_sleep(interval, initsleep, funcname)
    while True:
        try: func()
        except Exception as e:
            logger.warning(f"exception at {funcname} function")
            logger.warning(e)
        interval_sleep(interval, None, funcname)

def auto_reply(bot, interval, initsleep=None):
    funcname = sys._getframe().f_code.co_name
    run(lambda:bot.reply(), interval, initsleep, funcname)

def auto_tweets(bot, interval, initsleep=None):
    funcname = sys._getframe().f_code.co_name
    run(lambda:bot.auto_tweet(), interval, initsleep, funcname)

def auto_follows(bot, interval, initsleep=None):
    funcname = sys._getframe().f_code.co_name
    run(lambda:bot.auto_follow(), interval, initsleep, funcname)

if __name__ == '__main__':
    lock = threading.Lock()
    bot = EigoyurusanBot(lock, logger)
    
    #リプライ要のスレッド
    auto_reply_thread = threading.Thread(target=auto_reply, args=(bot,3*60))
    #自動ツイート用のスレッド
    auto_tweet_thread = threading.Thread(target=auto_tweets, args=(bot,60*60))
    #自動フォローバック用のスレッド
    auto_follow_thread = threading.Thread(target=auto_follows, args=(bot,3*60))

    auto_reply_thread.start()
    auto_tweet_thread.start()
    auto_follow_thread.start()
