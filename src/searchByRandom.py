import arxiv
import random
from translate import traslateBydeepL
from cat_list import cat_list


def searchByRandom(driver=None):
    num = int(random.random() * len(cat_list) + 1)
    if num >= len(cat_list):
        num = len(cat_list) - 1
    QUERY = "cat:'{}'".format(cat_list[num][0])
    result_list = arxiv.query(query=QUERY, max_results=100)
    resultlen = len(result_list)
    chosen_list = []

    if resultlen <= 4:
        for i in range(resultlen):
            chosen_list.append(result_list[i])
    else:
        tmp = [0]
        count = 1
        while count < 4:
            num = int(random.random() * resultlen + 1)
            if not (num in tmp) and num != resultlen:
                tmp.append(num)
                count += 1
        for i in tmp:
            chosen_list.append(result_list[i])

    Summary_list = []
    for result in chosen_list:
        Summary = {}
        Summary['title_EN'] = result.title.replace("\n", " ")
        Summary['title_JP'] = traslateBydeepL(Summary['title_EN'], lang='JA', driver)
        Summary['author'] = result.author
        Summary['pdf_url'] = result.pdf_url
        Summary['abs_url'] = result.arxiv_url
        Summary['date'] = result.updated[:10]
        Summary['abstract_EN'] = result.summary.replace("-\n", "").replace("\n", " ").replace(". ", ".\n")
        Summary['abstract_JP'] = traslateBydeepL(Summary['abstract_EN'], lang='JA', driver)

        Summary_list.append(Summary)
    return Summary_list, cat_list[num][1], cat_list[num][2]
