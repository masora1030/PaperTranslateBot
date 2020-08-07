import tweepy, os, time
import secret

class Twitter:
    def __init__(self, logger):
        auth = tweepy.OAuthHandler(secret.CK, secret.CS)
        auth.set_access_token(secret.AT, secret.AS)
        self.api = tweepy.API(auth)
        self.logger = logger
        # self.Twitter_ID = "eigoyurusan"
        # self.SCREEN_NAME = '英語論文速読bot'
        if os.path.exists('last_rep'):
            with open('last_rep') as f:
                self.last_reply_id = f.readline().rstrip()
        else: self.last_reply_id = None

    def followback(self):
        followers_obj = self.api.followers()
        followers = set([f.id for f in followers_obj if not f.follow_request_sent])
        friends = set([f.id for f in self.api.friends()])
        new = followers - friends

        id_dic = {f.id:f for f in followers_obj}
        for n in new: self.logger.info(f"new followers {id_dic[n].screen_name}")
        for n in new:
            self.try_create_friendship(n)
            time.sleep(20)

    def follow_if_not(self, id_):
        if id_ not in set([f.id for f in self.api.friends()]):
            self.try_create_friendship(id_)

    def upload_papers(self, directory):
        media_ids = [self.api.media_upload(directory+f).media_id for f in sorted(os.listdir(directory))]
        for f in os.listdir(directory): os.remove(directory+f)
        return media_ids

    def tweet(self, text, *, media_ids=[], reply_to=None):
        try:
            self.api.update_status(text, media_ids=media_ids, in_reply_to_status_id=reply_to)
        except Exception as e: self.logger.warning(e)
        if reply_to:
            self.last_reply_id = reply_to
            with open('last_rep','w') as f: f.write(f"{reply_to}")

    def get_mentions(self):
        if self.last_reply_id == None:
            return self.api.mentions_timeline(count=30)
        else: return self.api.mentions_timeline(count=200, since_id=self.last_reply_id)

    def get_mentions_custom(self):
        timeline = self.get_mentions()
        timeline = [status for status in timeline if len(status.entities["user_mentions"])==1]
        return timeline

    def try_create_favorite(self, id_):
        try: self.api.create_favorite(id_)
        except: self.logger.warning(f'failed to create favorite to {id_}')

    def try_create_friendship(self, id_):
        try: self.api.create_friendship(id_)
        except: self.logger.warning(f'failed to create friendship with {id_}')
