import imgkit
import os

# To convert HTML into a image
def makeJPG(HTML_list, TwitterID, path='reply'):
    now_path = os.path.dirname(os.path.abspath(__file__))
    filedir = f"{now_path}/images/{path}/{TwitterID}"
    os.makedirs(filedir, exist_ok=True)
    for i,html in enumerate(HTML_list):
        filepath = f"{filedir}/result_{i+1}.jpg"
        imgkit.from_string(html, filepath, options={'width':1300}) 

def makeHTML(Summary_list):
    retHTML = []
    for result in Summary_list:
        abstract_JP = result['abstract_JP'].replace('\n',"<br>")
        abstract_EN = result['abstract_EN'].replace('\n',"<br>")
        html = f"""<!DOCTYPE html>
        <html lang="ja">
            <head><meta charset="utf-8"></head>
            <body style="margin:50px">
                <h1 style="font-size:55px">{result['title_JP']}</h1>
                <p style="font-size:22px">{result['title_EN']}[{result['author']}]</p>
                <p style="font-size:30px">date:{result['date']}</p>
                <p style="font-size:40px">{abstract_JP}</p>
                <p style="font-size:22px">{abstract_EN}</p>
            </body>
        </html>
        """
        retHTML.append(html)
    return retHTML
