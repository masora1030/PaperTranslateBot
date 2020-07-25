'''Keyword search Module'''

from searchByKeyword import searchByKeyword
from makeHTML import makeHTML
from makeJPG import makeJPG

def getOutputByKeyword(TwitterID, keyward):
    Summary_list = searchByKeyword(keyward)
    HTML_list = makeHTML(Summary_list)
    makeJPG(HTML_list, TwitterID, path='reply')
    count = 0
    ret_list = []
    for result in Summary_list:
        count += 1
        ret = [result['title_JP'], result['abs_url']]
        ret_list.append(ret)
    return ret_list
