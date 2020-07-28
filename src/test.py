from DeeplDriver import Translate
import time

t = Translate()
i = t.put(text="could you help me",source_lang="EN", target_lang="JA")
text = t.get(i)
print(text)