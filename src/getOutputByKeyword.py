'''Keyword search Module'''

from searchByKeyword import searchByKeyword
from makeHTML import makeHTML
from makeJPG import makeJPG

def getOutputByKeyword(TwitterID, keyward, driver=None):
    Summary_list = searchByKeyword(keyward, driver=driver)
    HTML_list = makeHTML(Summary_list)
    makeJPG(HTML_list, TwitterID, path='reply')
    count = 0
    ret_list = []
    for result in Summary_list:
        count += 1
        ret = [result['title_JP'][:min(len(result['title_JP']), 20)], result['abs_url']]
        ret_list.append(ret)
    return ret_list
