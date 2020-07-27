# -*- coding: utf-8 -*-
import tweepy
import json
import os
import time
import threading

from getOutputByKeyword import *
from getOutputByRandom import *

import requests


class EigoyurusanBot():
    def __init__(self,api,Twitter_ID,SCREEN_NAME,lock):
        self.api = api
        self.Twitter_ID = Twitter_ID
        self.SCREEN_NAME = SCREEN_NAME
        self.lock = lock
        self.last_rep = ''

    def auto_follow(self):
        #新しい方から順番に20人取ってくる
        self.lock.acquire()
        followers = set([f.id for f in self.api.followers() if not f.follow_request_sent]) #count = 20
        friends = set([f.id for f in self.api.friends()])
        new = followers - friends
        if new: print("new followers", new)
        for n in new:
            self.api.create_friendship(n) #指定したidのuserをフォロー
            time.sleep(20)
        self.lock.release()

    def auto_tweet(self):
        '''
        Automatically tweets the content of papers
        searched for in random categories
        '''
        print("start auto tweet")
        self.lock.acquire()
        #Random search Module
        ret_cat, rlist = getOutputByRandom()

        length = int((280-len("\n".join([ret_cat[1]]+[f":{url}" for _,url in rlist])))/2/4)
        texts = [f"{ret_cat[1]}"]
        texts.extend([f">{title[:length-3]+'...' if len(title)>length else title}:{url}" for title,url in rlist])
        
        print("get image files")
        #画像ファイルの取得
        auto_path = './images/auto/eigoyurusan/'
        auto_file_names = os.listdir(auto_path)
        auto_media_ids = []

        for auto_filename in sorted(auto_file_names)[:len(rlist)]:
            auto_res = self.api.media_upload(auto_path + auto_filename)
            auto_media_ids.append(auto_res.media_id)
        text = "\n".join(texts)
        print(len(text))
        print(text)
        self.api.update_status(status=text, media_ids=auto_media_ids)
        self.lock.release()
        print("end auto tweet")


    #この関数を10分ごとに回す
    def reply(self):
        '''
        Get 200 replies to yourself in a tweet on
        the timeline and tweet an image of the
        resulting translation.
        '''
        if self.last_rep == '':
            timeline = self.api.mentions_timeline(count=1)
        else:
            timeline = self.api.mentions_timeline(count=200, since_id=self.last_rep)
        #その時のタイクラインの状況を取ってくる
        if len(timeline) == 0:#一つもなかった場合
            print("reply tweets doesn't exist.")
            return
        
        self.last_rep = timeline[0].id
        for status in timeline:
            screen_name = status.author.screen_name
            if status.author.id not in set([f.id for f in self.api.friends()]):
                self.api.create_friendship(status.author.id)
            #inpが相手の返信内容
            keywords = status.text.lstrip("@"+self.Twitter_ID).replace('\n','')#本文の余計な部分を削除
            print(f"keywords {keywords} are sent by {screen_name}")
            #Keyword search Module
            ret_list = getOutputByKeyword(screen_name, keywords)
            if len(ret_list)==0: continue
            #ツイート本文
            #self.reply_text="@"+self.screen_name.decode()+'検索キーワード -> '+self.inp+'\n'+'検索結果\n'
            length = int((280-len("\n".join([screen_name]+[f":{url}" for _,url in ret_list])))/2/4)
            texts = [f"@{screen_name}"]
            texts.extend([f">{title[:length-3]+'...' if len(title)>length else title}:{url}" for title,url in ret_list])
             
            self.lock.acquire()#api変数
            
            #画像ファイルの取得
            path = f'./images/reply/{screen_name}/' #ファイルディレクトリ
            file_names = os.listdir(path)#ファイルをリストで取得
            media_ids = []
            for filename in sorted(file_names)[:len(ret_list)]:
                res = self.api.media_upload(path + filename)
                media_ids.append(res.media_id) #idリストへ追加
            #ツイート
            text = "\n".join(texts)
            print(len(text))
            print(text)
            self.api.update_status(media_ids=media_ids, status=text, in_reply_to_status_id=status.id)
            self.lock.release()

