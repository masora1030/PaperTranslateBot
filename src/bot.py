# -*- coding: utf-8 -*-
from Twitter import Twitter
from Paper import Paper
from DeeplDriver import Translate
import emoji

class EigoyurusanBot():
    def __init__(self,lock):
        self.twitter = Twitter()
        translate = Translate()
        self.paper = Paper(translate)
        self.lock = lock

    def make_papers_text(self, titles:list, urls:list, *, prefix=''):
        if len("".join(titles))==0: prefix += "\n翻訳に失敗しました."

        length = len("\n".join([prefix] + [f'>{u} :' for u in urls]))
        title_length = (280 - length) // 8
        trim = lambda title:title if len(title)<=title_length else title[:title_length-2]+'..'
        text = "\n".join([prefix] + [f'>{u} :{trim(t)}' for u,t in zip(titles,urls)])
        return text

    def auto_follow(self):
        self.lock.acquire()
        self.twitter.followback()
        self.lock.release()

    def auto_tweet(self):
        '''
        Automatically tweets the content of papers
        searched for in random categories
        '''
        print("start auto tweet")
        self.lock.acquire()
        #Random search Module
        category, ret_list = self.paper.getOutputByRandom()
        urls, titles = zip(*ret_list)

        text = self.make_papers_text(titles, urls, prefix=f'#英許_{category[1]}')
        media_ids = self.twitter.upload_papers('./images/auto/eigoyurusan/')
        self.twitter.tweet(text, media_ids=media_ids)
        self.lock.release()
        print("end auto tweet")

    def reply(self):
        '''
        Get 200 replies to yourself in a tweet on
        the timeline and tweet an image of the
        resulting translation.
        '''
        timeline = self.twitter.get_mentions_custom()
        if len(timeline)==0: print("reply tweets doesn't exist."); return

        for status in reversed(timeline): self.twitter.try_create_favorite(status.id)
        for status in reversed(timeline):
            self.twitter.follow_if_not(status.author.id)
            screen_name = status.author.screen_name
            prefix = f"@{screen_name} "

            #inpが相手の返信内容
            keywords = status.text.replace('\n',' ').split(" ")
            keywords = [k for k in keywords if "@" not in k]
            keywords = "".join([c for c in keywords if c not in emoji.UNICODE_EMOJI])
            print(f"keywords {keywords} are sent by {screen_name}")

            #Keyword search Module
            ret_list, t_keyword = self.paper.getOutputByKeyword(screen_name, keywords)
            urls, titles = zip(*ret_list)

            self.lock.acquire()
            if len(ret_list)==0:
                print(f"no retlist, {t_keyword}")
                prefix += f'sorry no result for {t_keyword}'
                self.twitter.tweet(text, reply_to=status.id)
                continue

            if t_keyword != keywords:
                prefix += f":{t_keyword}" if len(t_keyword)<40 else f":{t_keyword[:37]}..."
            text = self.make_papers_text(titles, urls, prefix=prefix)
            print(text)
            media_ids = self.twitter.upload_papers(f'./images/reply/{screen_name}/')
            self.twitter.tweet(text, media_ids=media_ids, reply_to=status.id)

            self.lock.release()
