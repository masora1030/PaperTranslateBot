from selenium import webdriver
from selenium.webdriver.chrome import options, service
import time, os, random, shutil, queue, threading

class Translate:
    def __init__(self, logger):
        self.logger = logger
        self.dDriver = DeeplDriver(logger)
        self.queue = queue.Queue()
        self.results = {}
        threading.Thread(target=self.process).start()

    def __call__(self, text, **kwargs):
        kwargs['text'] = text
        id_ = self.put(**kwargs)
        return self.get(id_)

    def put(self, **kwargs):
        id_ = str(int(time.time()*100000000))+str(random.randint(0,99))
        kwargs["id_"] = id_
        self.queue.put(kwargs)
        return id_

    def get(self, id_):
        while id_ not in self.results.keys():
            time.sleep(1)
        res = self.results[id_]
        del self.results[id_]
        return res

    def process(self):
        while True:
            obj = self.queue.get()
            id_ = obj['id_']
            self.logger.info(f'processing translate {id_}')
            del obj['id_']
            res = self.dDriver.translate(**obj)
            self.results[id_] = res

class DeeplDriver:
    def __init__(self,logger):
        self.logger = logger
        options_ = options.Options()
        options_.headless = True
        if not shutil.which("chromedriver"): raise Exception('please install chromedriver')
        path = shutil.which("chromedriver")
        service_ = service.Service(path)
        self.driver = webdriver.Chrome(service=service_, options=options_)
        base = '//*[@id="dl_translator"]/div[1]'
        source = f'{base}/div[3]'
        target = f'{base}/div[4]'
        self.source_lang = f'{source}/div[1]'
        self.target_lang = f'{target}/div[1]/div[1]'
        self.source_lang_button = f'{self.source_lang}/div[1]/button'
        self.target_lang_button = f'{self.target_lang}/div[1]/button'
        self.source_textarea = f'{source}/div[2]/div[1]/textarea'
        self.target_textarea = f'{target}/div[3]/div[1]/textarea'
        self.initialize()

    def initialize(self):
        self.driver.get("https://www.deepl.com/ja/translator")
        self.driver.implicitly_wait(2)
        self._find('//*[@id="dl_cookieBanner"]/div[1]/div[1]/div[1]/span/div[2]/button')[0].click()
        self.driver.implicitly_wait(1)
        self.put_source("")
        self.driver.implicitly_wait(1)

    def __del__(self): self.driver.close()

    def _find(self, xpath):
        return self.driver.find_elements_by_xpath(xpath)
    def has_class(self, classname):
        return classname in self._find('//*[@id="dl_translator"]')[0].get_attribute('class').split(" ")
    def is_busy(self):
        return self.has_class("lmt--active_translation_request")
    def is_finished(self):
        return self.has_class("lmt--showing_alternatives")
    def is_long_text(self):
        return self.has_class("lmt--very_long_text")
    def is_empty(self):
        return self.has_class("lmt--empty_source")
    def wait_translate(self):
        time.sleep(0.1)
        while self.is_busy():
            while self.is_busy(): time.sleep(0.1)
            time.sleep(1)
        
    def get_selected_source_lang(self):
        return self._find(f'{self.source_lang_button}/span/strong')[0].text
    def get_selected_target_lang(self):
        return self._find(f'{self.target_lang_button}/span/strong')[0].text

    # langs are ['auto'(source-only), 'JA', 'EN', 'DE', 'FR', 'ES', 'PT', 'IT', 'NL', 'PL', 'RU', 'ZH']
    def select_lang(self, lang, button_path):
        self._find(f'{button_path}/button')[0].click()
        time.sleep(1.5)
        buttons = self._find(f'{button_path}/div/button')
        langs = [button.get_attribute('dl-lang') for button in buttons]
        if lang not in langs: raise Exception(f'lang {lang} is not found')
        self._find(f'{button_path}/div/button')[langs.index(lang)].click()
        time.sleep(1)
    def select_source_lang(self,lang):
        self.select_lang(lang, f'{self.source_lang}/div[1]')
    def select_target_lang(self,lang):
        self.select_lang(lang, f'{self.target_lang}/div[1]')

    def put_source(self,text):
        textarea = self._find(self.source_textarea)[0]
        textarea.clear()
        textarea.send_keys(text)
        pre = None
        while True:
            tmp = self.get_source()
            if tmp == pre: break
            pre = tmp
            time.sleep(0.5)

    def get_source(self):
        textarea = self._find(self.source_textarea)[0]
        return textarea.get_attribute('value')
    def get_target(self):
        textarea = self._find(self.target_textarea)[0]
        return textarea.get_attribute('value')

    def _translate(self, text, source_lang, target_lang):
        self.select_source_lang(source_lang)
        self.put_source("")
        self.put_source(text)
        self.wait_translate()
        langdic = {'JA':'日本語','EN':'英語','RU':'ロシア語','PL':'ポーランド語','NL':'オランダ語',
            'IT':'イタリア語','PT':'ポルトガル語','ES':'スペイン語','FR':'フランス語','DE':'ドイツ語','ZH':'中国語'}
        if source_lang == "auto" and self.get_selected_source_lang() == langdic[target_lang]: return text
        
        if self.get_selected_target_lang() != langdic[target_lang]:
            self.select_target_lang(target_lang)
            time.sleep(0.5)

        self.wait_translate()
        translated = self.get_target()
        return translated

    def translate(self, text, source_lang='auto', target_lang="JA"):
        for i in range(4):
            try:
                translated = self._translate(text, source_lang, target_lang)
                return translated
            except Exception as e:
                self.logger.warning(f"failed to translate, {i} times")
                self.logger.warning(e)
                self.initialize()
        raise Exception("failed to translate")
