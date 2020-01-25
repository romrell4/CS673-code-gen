import requests
from webscraping import web_scraper

def get_css_stats(url):
    html = web_scraper.get_html(url)
    print(html)

if __name__ == '__main__':
    get_css_stats("test.html")