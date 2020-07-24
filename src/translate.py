'''Translate Module'''

import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from makeJPG import makeJPG
from get_driver import get_driver

now_path = os.path.dirname(os.path.abspath(__file__))
driver_path = now_path + '/chromedriver'

lang_button_path = {'RU':'//*[@id="dl_translator"]/div[1]/div[4]/div[1]/div[1]/div[1]/div/button[11]', # ロシア
                    'PL':'//*[@id="dl_translator"]/div[1]/div[4]/div[1]/div[1]/div[1]/div/button[10]', # ポーランド
                    'NL':'//*[@id="dl_translator"]/div[1]/div[4]/div[1]/div[1]/div[1]/div/button[9]', # オランダ
                    'IT':'//*[@id="dl_translator"]/div[1]/div[4]/div[1]/div[1]/div[1]/div/button[8]', # イタリア
                    'PT':'//*[@id="dl_translator"]/div[1]/div[4]/div[1]/div[1]/div[1]/div/button[6]', # ポルトガル
                    'ES':'//*[@id="dl_translator"]/div[1]/div[4]/div[1]/div[1]/div[1]/div/button[5]', # スペイン
                    'FR':'//*[@id="dl_translator"]/div[1]/div[4]/div[1]/div[1]/div[1]/div/button[4]', # フランス
                    'DE':'//*[@id="dl_translator"]/div[1]/div[4]/div[1]/div[1]/div[1]/div/button[3]', # ドイツ
                    'EN':'//*[@id="dl_translator"]/div[1]/div[4]/div[1]/div[1]/div[1]/div/button[2]'} #  英語

def traslateBydeepL(input_text, lang='JA', driver=None):
    if input_text == '' or input_text == ' ' or input_text == '\n':
        return ''

    if driver == None:
        driver = get_driver()

    # DeepLクエリ
    baseURL = "https://www.deepl.com/ja/translator"
    # 返り値
    ret = ''

    # DeepLクエリ送信
    driver.get(baseURL)

    # 多言語対応
    if lang != 'JA':
        choice_button = \
        driver.find_elements_by_xpath('//*[@id="dl_translator"]/div[1]/div[4]/div[1]/div[1]/div[1]/button')[0]
        choice_button.click()
        sleep(1)
        lang_button = driver.find_elements_by_xpath(lang_button_path[lang])[0]
        lang_button.click()

    # 入力窓にテキスト送信
    input_element = driver.find_elements_by_xpath('//*[@id="dl_translator"]/div[1]/div[3]/div[2]/div[1]/textarea')
    input_element[0].send_keys(input_text)

    # 読み込み待ち
    if len(input_text) < 1000:
        sleep(5)
    else:
        sleep(8)

    # 出力窓からテキスト抽出
    output_element = driver.find_elements_by_xpath('//*[@id="dl_translator"]/div[1]/div[4]/div[3]/div[1]/textarea')
    for e in output_element:
        ret += e.get_attribute('value')

    return ret
