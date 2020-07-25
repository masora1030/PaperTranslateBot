'''Category search Module'''

from searchByCategory import searchByCategory
from makeHTML import makeHTML
from makeJPG import makeJPG

def getOutputByCategory(TwitterID, category):
    Summary_list, ce, cj = searchByCategory(category)
    ret_cat = [ce, cj]
    HTML_list = makeHTML(Summary_list)
    makeJPG(HTML_list, TwitterID, path='register')
    count = 0
    ret_list = []
    for result in Summary_list:
        count += 1
        ret = [result['title_JP'], result['abs_url']]
        ret_list.append(ret)
    return ret_cat, ret_list
