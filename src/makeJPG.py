import imgkit
import os

# To convert HTML into a image
def makeJPG(HTML_list, TwitterID, path='reply'):
    now_path = os.path.dirname(os.path.abspath(__file__))
    filedir = "{}/images/{}/{}".format(now_path, path, TwitterID)
    os.makedirs(filedir, exist_ok=True)
    for i,html in enumerate(HTML_list):
        filepath = "{}/result_{}.jpg".format(filedir, i+1)
        imgkit.from_string(html, filepath)