import arxiv
import random
from src.translate import traslateBydeepL
from src.cat_list import cat_list
import sys


def searchByCategory(category):
    num = -1
    for i, cat in enumerate(cat_list):
        if category == cat_list[0]:
            num = i
            break
    if num == -1:
        print('Error: DO NOT SUPPORT this category', file=sys.stderr)
        sys.exit(1)
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
        Summary['title_JP'] = traslateBydeepL(Summary['title_EN'], lang='JA')
        Summary['author'] = result.author
        Summary['pdf_url'] = result.pdf_url
        Summary['abs_url'] = result.arxiv_url
        Summary['date'] = result.updated[:10]
        Summary['abstract_EN'] = result.summary.replace("-\n", "").replace("\n", " ").replace(". ", ".\n")
        Summary['abstract_JP'] = traslateBydeepL(Summary['abstract_EN'], lang='JA')

        Summary_list.append(Summary)
    return Summary_list, cat_list[num][1], cat_list[num][2]