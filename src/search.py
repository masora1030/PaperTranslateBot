import arxiv
import random, datetime, time
from translate import traslateBydeepL

def search_random(query):

    def get_randomdate(year):
        startdate = datetime.datetime(year, 1, 1).timestamp()
        enddate = int(datetime.datetime.now().timestamp())-1000000
        start = datetime.datetime.fromtimestamp(random.randint(startdate,enddate)).strftime('%Y%m%d')
        end = start+"235959"
        return start, end

    results = []
    for i in range(10):
        start, end = get_randomdate(2019 if i<=2 else 2010)
        query_ = f"{query} AND submittedDate:[{start} TO {end}]"
        ret = arxiv.query(query=query_, max_results=1)
        if ret and sum([r.pdf_url==ret[0].pdf_url for r in results])==0: results.append(ret[0])
        if len(results) >= 4: break
    
    return shaping(results)

def search_n_random(query, n):
    ret = arxiv.query(query=query, max_results=n)
    results = random.sample(ret, 4) if len(ret)>=4 else ret
    return shaping(results)
    
def shaping(results):
    return [
            {
                "title_EN": res.title.replace('\n',' '),
                "title_JP": traslateBydeepL(res.title.replace('\n',' '), lang="JA"),
                "author":   res.author,
                "pdf_url":  res.pdf_url.replace('http://',''),
                "abs_url":  res.arxiv_url.replace('http://',''),
                "date":     res.updated[:10],
                "abstract_EN": res.summary.replace('-\n',"").replace("\n"," ").replace(". ",".\n"),
                "abstract_JP": traslateBydeepL(res.summary.replace('\n',' '), lang="JA")
            }
            for res in results
        ]
