import imgkit
import os

# To convert HTML into a image
def makeJPG(HTML_list, TwitterID, path='reply'):
    now_path = os.path.dirname(os.path.abspath(__file__))
    filedir = f"{now_path}/images/{path}/{TwitterID}"
    os.makedirs(filedir, exist_ok=True)
    for i,html in enumerate(HTML_list):
        filepath = f"{filedir}/result_{i+1}.jpg"
        imgkit.from_string(html, filepath, options={'width':650})
        
