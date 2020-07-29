from DeeplDriver import Translate
import time

t = Translate()
text = t(text="could you help me",source_lang="EN", target_lang="JA")
print(text)


time.sleep(10)
text = t(text="私はあないあ",source_lang="EN", target_lang="JA")
print(text)
time.sleep(1)
text = t(text="そして食べられる",source_lang="EN", target_lang="JA")
print(text)