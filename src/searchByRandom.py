import random
from cat_list import cat_list
from search import search_random

def searchByRandom():
    num = int(random.random() * len(cat_list) + 1)
    if num >= len(cat_list):
        num = len(cat_list) - 1

    return search_random(f"cat:'{cat_list[num][0]}'"), cat_list[num][1], cat_list[num][2]
