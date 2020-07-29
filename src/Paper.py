from Search import Search
from Shaping import makeHTML, makeJPG

class Paper:
    def __init__(self, translate):
        self.translate = translate
        self.search = Search(translate)

    def getOutputByCategory(self, TwitterID, category):
        Summary_list, ce, cj = self.search.searchByCategory(category)
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

    def getOutputByKeyword(self, TwitterID, keyward):
        Summary_list, t_keyword = self.search.searchByKeyword(keyward)
        HTML_list = makeHTML(Summary_list)
        makeJPG(HTML_list, TwitterID, path='reply')
        count = 0
        ret_list = []
        for result in Summary_list:
            count += 1
            ret = [result['title_JP'], result['abs_url']]
            ret_list.append(ret)
        return ret_list, t_keyword

    def getOutputByRandom(self):
        TwitterID = 'eigoyurusan'
        Summary_list, ce, cj = self.search.searchByRandom()
        ret_cat = [ce, cj]
        HTML_list = makeHTML(Summary_list)
        makeJPG(HTML_list, TwitterID, path='auto')
        count = 0
        ret_list = []
        for result in Summary_list:
            count += 1
            ret = [result['title_JP'], result['abs_url']]
            ret_list.append(ret)
        return ret_cat, ret_list
