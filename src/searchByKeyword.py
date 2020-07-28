import re
import random
from search import search_random
from translate import traslateBydeepL

def searchByKeyword(input_str):
    if not (re.findall('^[a-zA-Z1-9 .\',!\?#]+$', input_str)):
        input_str = traslateBydeepL(input_str, force_to_en=True)
    query = "all:'{}'".format(input_str)
    
    return search_random(query), input_str
