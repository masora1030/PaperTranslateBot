import random
from cat_list import cat_list
import sys
from search import search_random

def searchByCategory(category):
    num = -1
    for i, cat in enumerate(cat_list):
        if category == cat_list[0]:
            num = i
            break
    if num == -1:
        print('Error: DO NOT SUPPORT this category', file=sys.stderr)
        sys.exit(1)
    query = "cat:'{}'".format(cat_list[num][0])

    return search_random(query), cat_list[num][1], cat_list[num][2]
