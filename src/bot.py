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

    def auto_tweet(self):
        '''
        Automatically tweets the content of papers
        searched for in random categories
        '''
        print("start auto tweet")
        self.lock.acquire()
        #Random search Module
        self.ret_cat, self.rlist = getOutputByRandom()
        self.text = "["+self.ret_cat[1]+"]\n"
        for self.i,self.r in enumerate(self.rlist):
            self.text += '・'+self.r[0]
            if len(self.r[0])>20:
                self.text += '... :'+self.r[1]+'\n'
            else:
                self.text += ':'+self.r[1]+'\n'

        print("get image files")
        #画像ファイルの取得
        self.auto_path = './images/auto/eigoyurusan/'
        self.auto_file_names = os.listdir(self.auto_path)
        self.auto_media_ids = []

        for self.auto_filename in sorted(self.auto_file_names):
            print(self.auto_filename)
            self.auto_res = self.api.media_upload(self.auto_path+self.auto_filename)
            self.auto_media_ids.append(self.auto_res.media_id)
        print(len(self.text))
        print(self.text)
        self.api.update_status(status = self.text,
                                media_ids= self.auto_media_ids)
        self.lock.release()
        print("end auto tweet")


    #この関数を10分ごとに回す
    def reply(self):
        '''
        Get 200 replies to yourself in a tweet on
        the timeline and tweet an image of the
        resulting translation.
        '''

        self.timeline = self.api.mentions_timeline(count = 200)
        #その時のタイクラインの状況を取ってくる
        if len(self.timeline) == 0:#一つもなかった場合
            print("The reply tweet doesn't exist.")
            return False
        else:
            for self.status in self.timeline:#10分以内来たリプライを10分ごとに返すことによって、二重リプライを避ける
                self.nowTime = time.time()#現在の時間
                self.mentionTime = self.status.created_at.timestamp()#ツイートがされた時の時間

                if self.nowTime - self.mentionTime < 33000.0:
                    self.status_id=self.status.id#ステータスid
                    self.screen_name=self.status.author.screen_name.encode("UTF-8")
                    self.scrn = self.screen_name.decode().replace(' ', '')
                    self.scr = self.scrn.rstrip('\n')#最後の改行
                    #inpが相手の返信内容
                    self.inp = self.status.text.lstrip("@"+self.Twitter_ID)#本文の余計な部分を削除
                    self.inp = self.inp.replace('\n','')#改行は無視

                    self.lock.acquire()#api変数,driverを使用するのでロック

                    #Keyword search Module
                    self.ret_list = getOutputByKeyword(self.screen_name.decode(),self.inp)

                    #ツイート本文
                    self.reply_text="@"+self.screen_name.decode()+'検索キーワード -> '+self.inp+'\n'+'検索結果\n'
                    for self.j,self.rl in enumerate(self.ret_list):
                        self.reply_text += '・'+self.rl[0]
                        if len(self.rl[0])>20:
                            self.reply_text += '... :'+self.rl[1]+'\n'
                        else:
                            self.reply_text += ':'+self.rl[1]+'\n'


                    #画像ファイルの取得
                    self.path = './images/reply/'+self.screen_name.decode()#ファイルディレクトリ
                    self.file_names = os.listdir(self.path)#ファイルをリストで取得
                    self.media_ids = []
                    for self.filename in sorted(self.file_names):
                        print(self.filename)
                        self.res = self.api.media_upload(self.path+'/'+self.filename)
                        self.media_ids.append(self.res.media_id)#idリストへ追加
                    #ツイート
                    print(len(self.reply_text))
                    print(self.reply_text)
                    self.api.update_status(media_ids=self.media_ids,
                                            status=self.reply_text,
                                            in_reply_to_status_id=self.status_id)
                    self.lock.release()

