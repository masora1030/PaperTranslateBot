'''Category search Module'''

from src.searchByCategory import searchByCategory
from src.makeHTML import makeHTML
from src.makeJPG import makeJPG

def getOutputByCategory(TwitterID, category):
    Summary_list, ce, cj = searchByCategory(category)
    ret_cat = [ce, cj]
    HTML_list = makeHTML(Summary_list)
    makeJPG(HTML_list, TwitterID, path='register')
    count = 0
    ret_list = []
    for result in Summary_list:
        count += 1
        ret = [result['title_JP'][:min(len(result['title_JP']), 20)], result['abs_url']]
        ret_list.append(ret)
    return ret_cat, ret_list