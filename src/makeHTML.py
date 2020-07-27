# markdown, html生成

import markdown


def makeHTML(Summary_list):
    retMD = []
    retHTML = []
    for result in Summary_list:
        md = ''
        md = ''.join([md, '# ', result['title_JP']])
        md = ''.join([md, '\n'])
        md = ''.join([md, '## ', result['title_EN']])
        md = ''.join([md, '\n'])
        md = ''.join([md, '### ', result['author']])
        md = ''.join([md, '\n'])
        md = ''.join([md, '### ', 'date:', result['date']])
        md = ''.join([md, '\n'])
        md = ''.join([md, '### ', '[概要]'])
        md = ''.join([md, '\n', result['abstract_JP'].replace("\n", "<br>")])
        md = ''.join([md, '\n'])
        md = ''.join([md, '### ', '[Abstract]'])
        md = ''.join([md, '\n', result['abstract_EN'].replace("\n", "<br>")])
        md = ''.join([md, '\n'])
        retMD.append(md)

    for mdtext in retMD:
        md = markdown.Markdown(extensions=['admonition', 'footnotes'])
        body = md.convert(mdtext)
        html = '<html lang="ja"><meta charset="utf-8"><body>'
        html += body
        html += '</body></html>'
        retHTML.append(html)

    return retHTML
