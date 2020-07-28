from selenium import webdriver
from selenium.webdriver.chrome import options, service
import time, os, random
import shutil, queue

class Translate:
    def __init__(self):
        self.dDriver = DeeplDriver()
        self.queue = queue.Queue()
        self.results = {}

    def put(self, **kwargs):
        id_ = time.time() + random.randint(0,100)
        self.queue.put(id_=id_, **kwargs)
        return id_

    def get(self, id_):
        while not self.results[id_]:
            time.sleep(0.1)
        res = self.results[id_]
        return res

    def process(self):
        while True:
            obj = self.queue.get()
            id_ = obj
            print(f'processing {id_}')
            del obj['id_']
            res = self.dDriver.translate(**obj)
            self.results[id_] = res

class DeeplDriver:
    def __init__(self):
        options_ = options.Options()
        # options_.add_argument('--headless')
        options_.headless = True
        # if not shutil.which("chromedriver"): raise Exception('please install chromedriver')
        # path = shutil.which("chromedriver")
        path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"
        service_ = service.Service(path)
        self.driver = webdriver.Chrome(service=service_, options=options_)
        self.driver.get("https://www.deepl.com/ja/translator")

        base = '//*[@id="dl_translator"]/div[1]'
        source = f'{base}/div[3]'
        target = f'{base}/div[4]'
        self.source_lang = f'{source}/div[1]'
        self.target_lang = f'{target}/div[1]'
        self.source_lang_button = f'{self.source_lang}/div[1]/button'
        self.target_lang_button = f'{self.target_lang}/div[1]/button'
        self.source_textarea = f'{source}/div[2]/div[1]/textarea'
        self.target_textarea = f'{target}/div[3]/div[1]/textarea'

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
        while self.is_busy(): time.sleep(0.1)

    def detect_lang(self, text):
        self._find(self.source_textarea)[0].send_keys(text)
        self.wait_translate()
        return self._find(f'{self.source_lang_button}/span/strong')[0].text

    # langs are ['auto'(source-only), 'JA', 'EN', 'DE', 'FR', 'ES', 'PT', 'IT', 'NL', 'PL', 'RU', 'ZH']
    def select_lang(self, lang, button_path):
        self._find(f'{button_path}/button')[0].click()
        self.wait_translate()
        buttons = self._find(f'{button_path}/div/button')
        langs = [button.get_attribute('dl-lang') for button in buttons]
        if lang not in langs: raise Exception(f'lang {lang} is not found')
        try: self._find(f'{button_path}/div/button')[langs.index(lang)].click()
        except: raise Exception('failed to click when selecting language')
    def select_source_lang(self,lang):
        self.select_lang(lang, f'{self.source_lang}/div[1]')
    def select_target_lang(self,lang):
        self.select_lang(lang, f'{self.target_lang}/div[1]/div[1]')

    def put_source(self,text):
        textarea = self._find(self.source_textarea)[0]
        textarea.clear()
        textarea.send_keys(text)
    def get_target(self):
        textarea = self._find(self.target_textarea)
        return "".join([e.get_attribute('value') for e in textarea])

    def translate(self, text, source_lang='auto', target_lang="JA"):
        if source_lang == "auto" and self.detect_lang(text) == target_lang: return text

        self.select_source_lang(source_lang)
        self.select_target_lang(target_lang)
        self.put_source(text)
        self.wait_translate()
        translated = self.get_target()
        return translated