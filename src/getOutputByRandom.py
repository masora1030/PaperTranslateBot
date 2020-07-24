'''Random search Module'''

from searchByRandom import searchByRandom
from makeHTML import makeHTML
from makeJPG import makeJPG

def getOutputByRandom(driver=None):
    TwitterID = 'eigoyurusan'
    Summary_list, ce, cj = searchByRandom(driver)
    ret_cat = [ce, cj]
    HTML_list = makeHTML(Summary_list)
    makeJPG(HTML_list, TwitterID, path='auto')
    count = 0
    ret_list = []
    for result in Summary_list:
        count += 1
        ret = [result['title_JP'][:min(len(result['title_JP']), 20)], result['abs_url']]
        ret_list.append(ret)
    return ret_cat, ret_list
