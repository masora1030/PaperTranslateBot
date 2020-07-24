import re
import random
from search import search_random
from translate import traslateBydeepL

def searchByKeyword(input_str):
    if not (re.findall('^[a-zA-Z .\',!\?#]+$', input_str)):
        input_str = traslateBydeepL(input_str, lang='EN')
    query = "all:'{}'".format(input_str)
    
    return search_random(query)
