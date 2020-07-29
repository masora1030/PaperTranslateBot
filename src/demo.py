from bot import *
import sys, time, datetime, logging, threading

def init_sleep(interval, initsleep, funcname):
    if initsleep==None:
        now = datetime.datetime.now()
        initsleep = interval-(now.minute*60+now.second+now.microsecond/100000)%interval
    print(f'[{funcname}] initial sleep: {initsleep} s')
    time.sleep(initsleep)
    print(f"[{funcname}] started at {datetime.datetime.now()}")

def run(func, interval, funcname):
    while True:
        func()
        # try: func()
        # except Exception as e:
        #     print(f"exception at {funcname} function")
        #     print(e)
        time.sleep(interval)

def auto_reply(bot, interval, initsleep=None):
    funcname = sys._getframe().f_code.co_name
    init_sleep(interval, initsleep, funcname)
    run(lambda:bot.reply(), interval, funcname)

def auto_tweets(bot, interval, initsleep=None):
    funcname = sys._getframe().f_code.co_name
    init_sleep(interval, initsleep, funcname)
    run(lambda:bot.auto_tweet(), interval, funcname)

def auto_follows(bot, interval, initsleep=None):
    funcname = sys._getframe().f_code.co_name
    init_sleep(interval, initsleep, funcname)
    run(lambda:bot.auto_follow(), interval, funcname)

if __name__ == '__main__':
    lock = threading.Lock()
    bot = EigoyurusanBot(lock)

    #リプライ要のスレッド
    auto_reply_thread = threading.Thread(target=auto_reply, args=(bot,5*60,0))
    #自動ツイート用のスレッド
    auto_tweet_thread = threading.Thread(target=auto_tweets, args=(bot,60*60))
    #自動フォローバック用のスレッド
    auto_follow_thread = threading.Thread(target=auto_follows, args=(bot,5*60))

    auto_reply_thread.start()
    auto_tweet_thread.start()
    auto_follow_thread.start()
