import arxiv
import random, datetime, time, re
from cat_list import cat_list

class Search:
    def __init__(self, logger, translate):
        self.logger = logger
        self.translate = translate

    def searchByRandom(self):
        num = int(random.random() * len(cat_list) + 1)
        if num >= len(cat_list):
            num = len(cat_list) - 1
        return self.search_random(f"cat:'{cat_list[num][0]}'"), cat_list[num][1], cat_list[num][2]

    def searchByKeyword(self, input_str):
        if not (re.findall('^[a-zA-Z1-9 .\',!\?#]+$', input_str)):
            input_str = self.translate(input_str, target_lang="EN")
        query = "all:'{}'".format(input_str)
        return self.search_n(query, 4), input_str

    def searchByCategory(self, category):
        en_catlist = list(map(lambda x:x[0], cat_list))
        if category not in en_catlist:
            raise Exception("DO NOT SUPPORT this category")
        i = en_catlist.index(category)
        query = "cat:'{}'".format(cat_list[i][0])
        return self.search_n_random(query,10), cat_list[i][1], cat_list[i][2]

    def search_random(self, query):
        def get_randomdate(year):
            startdate = datetime.datetime(year, 1, 1).timestamp()
            enddate = int(datetime.datetime.now().timestamp())-1000000
            start = datetime.datetime.fromtimestamp(random.randint(startdate,enddate)).strftime('%Y%m%d')
            end = (datetime.date.today()-datetime.timedelta(days=2)).strftime('%Y%m%d')+"235959"
            return start, end

        results = []
        for i in range(10):
            start, end = get_randomdate(2019 if i<=2 else 2010 if i<=7 else 1975)
            query_ = f"{query} AND submittedDate:[{start} TO {end}]"
            self.logger.info(query_)
            ret = arxiv.query(query=query_, max_results=5)
            for ret_ in ret:
                if sum([r.pdf_url==ret_.pdf_url for r in results])==0: 
                    results.append(ret_)
                    break
            if len(results) >= 4: break
        
        return self.shaping(results)

    def search_n_random(self, query, n):
        self.logger.info(query)
        ret = arxiv.query(query=query, max_results=n)
        results = random.sample(ret, 4) if len(ret)>=4 else ret
        return self.shaping(results)

    def search_n(self, query, n):
        self.logger.info(query)
        ret = arxiv.query(query=query, max_results=n)
        return self.shaping(ret)
        
    def shaping(self, results):
        shaped = []
        for res in results:
            title_EN = res.title.replace('\n',' ')
            title_JP = self.translate(title_EN, target_lang="JA")
            abstract_EN = res.summary.replace("-\n", "").replace("\n", " ").replace(". ", ".\n").replace("$", "")
            abstract_JP = self.translate(abstract_EN, target_lang="JA")
            shaped.append({
                        "title_EN": title_EN,
                        "title_JP": title_JP,
                        "author":   res.author,
                        "pdf_url":  res.pdf_url.replace('http://',''),
                        "abs_url":  res.arxiv_url.replace('http://',''),
                        "date":     res.updated[:10],
                        "abstract_EN": abstract_EN,
                        "abstract_JP": abstract_JP
                    })
        return shaped
