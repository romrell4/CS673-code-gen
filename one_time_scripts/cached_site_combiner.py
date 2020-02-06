from glob import glob
from bs4 import BeautifulSoup
import re

folders = glob('../cached_sites/*')

for folder in folders:
    with open(f'{folder}/index.html') as html_file:
        html = html_file.read()
    with open(f'{folder}/style.css') as css_file:
        css = css_file.read()

    css = re.sub('<!doctype HTML>.*</html>', '', css, flags=re.DOTALL | re.MULTILINE | re.IGNORECASE)

    soup = BeautifulSoup(html, "lxml")
    [x.extract() for x in soup.findAll('link', {'rel': "stylesheet"})]

    style_tag = soup.new_tag('style')
    style_tag.string = css
    try:
        soup.head.insert(0, style_tag)
    except:
        soup.insert(0, soup.new_tag('head'))
        soup.head.insert(0, style_tag)

    with open(f'{folder}/combined.html', 'w') as html_file:
        print(str(soup), file=html_file)
