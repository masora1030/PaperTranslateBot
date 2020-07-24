import arxiv
import random, datetime
from translate import traslateBydeepL
from cat_list import cat_list


def searchByRandom():
    num = int(random.random() * len(cat_list) + 1)
    if num >= len(cat_list):
        num = len(cat_list) - 1

    def get_randomdate():
        startdate = datetime.datetime(2010, 1, 1).timestamp()
        enddate = int(datetime.datetime.now().timestamp())
        start = datetime.datetime.fromtimestamp(random.randint(startdate,enddate)).strftime('%Y%m%d')
        end = start+"235959"
        return start, end

    results = []
    for _ in range(20):
        start, end = get_randomdate()
        QUERY = f"cat:'{cat_list[num][0]}' AND submittedDate:[{start} TO {end}]'"
        ret = arxiv.query(query=QUERY, max_results=1)
        if len(ret): results.append(ret[0])
        if len(results) >= 4: break

    shaped = [
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
    return shaped, cat_list[num][1], cat_list[num][2]
