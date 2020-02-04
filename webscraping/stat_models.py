from typing import Tuple
from copy import deepcopy, copy
import tinycss2
from bs4 import BeautifulSoup
from tinycss2.ast import ParseError
import random
from webscraping import web_scraper
from http.server import HTTPServer, SimpleHTTPRequestHandler
import tempfile
import _thread
import time


class HTML:
    """
    Class used to represent the DOM of a web page

    Attributes:
        soup (BeautifulSoup): the soup containing the parsed HTML
        tags ([str]): all unique tags used on the web page
        ids ([str]): all unique ids used on the web page
        classes ([str]): all unique classes used on the web page
    """

    def __init__(self, soup: BeautifulSoup = None, url: str = None):
        if url is not None:
            self.soup = web_scraper.get_soup(url)
        else:
            self.soup = soup
        all_tags = soup.find_all()
        self.tags = set([tag.name for tag in all_tags])
        self.ids = set([tag["id"] for tag in all_tags if tag.get("id") is not None])
        self.classes = set([klass for tag in all_tags if tag.get("class") is not None for klass in tag["class"]])

class CSS:
    """
    Class used to represent the style of a web page

    Attributes:
        selectors ([str: [str: str]): dictionary of selector (e.g. "thead" or "p#some-id") to the key-value pairs of rules (e.g. "font-size": "18pt")
    """

    def __init__(self, html_soup: BeautifulSoup=None, print_issues = False, url: str = None):
        if url is not None:
            html_soup = web_scraper.get_soup(url)
        self.print_issues = print_issues
        self.selectors = {}
        for style in html_soup.find_all("style"):
            stylesheet = tinycss2.parse_stylesheet(style.text, skip_comments = True, skip_whitespace = True)
            for rule_set in stylesheet:
                # If the prelude contains a comma, there are multiple selectors
                for selector in tinycss2.serialize(rule_set.prelude).split(","):
                    selector = selector.strip()
                    if selector not in self.selectors:
                        self.selectors[selector] = {}
                    # Update the current dictionary, overwriting conflicting keys
                    declarations = tinycss2.parse_declaration_list(rule_set.content, skip_comments = True, skip_whitespace = True)
                    self.selectors[selector].update({declaration.lower_name: tinycss2.serialize(declaration.value).strip() for declaration in declarations if type(declaration) != ParseError})
    
    def evaluate(self):
        # TODO: Actually evaluate the quality of CSS based on global stats or some metrics
        return 1

    def generate_css(self) -> str:
        rules = ""
        for k,v in self.selectors.items():
            rules += f"{k} {v}\n"
        return rules


class WebPage:
    """
    Class used to represent a web page

    Attributes:
        html (HTML): info about the HTML of the web page
        css (CSS): info about the CSS of the web page
    """
    photo_eval_limit = .5
    css_eval_limit = .7

    def __init__(self, url:str=None, html:HTML=None):
        if url is not None:
            soup = web_scraper.get_soup(url)
            self.html = HTML(soup)
            self.css = CSS(soup)
        elif html is not None:
            self.html = html
            self.css = None
        else:
            raise ArgumentError("Invalid Arguments")

    def generate_web_page(self) -> bytes:
        webpage = copy(self.html.soup)
        style_tag = webpage.new_tag('style')
        style_tag.string = self.css.generate_css()
        try:
            webpage.head.insert(0, style_tag)
        except:
            webpage.insert(0, soup.new_tag('head'))
            webpage.head.insert(0, style_tag)
        return webpage.encode()

    def gen_photo(self, saveLoc:str) -> str:
        photo = None
       
        with open("index.html", 'wb+') as indexFile:
            indexFile.write(self.generate_web_page())
            indexFile.flush()
        httpd = HTTPServer(('',8000), CustomHTTPRequestHandler)
        thd = _thread.start_new_thread(run_server, (httpd, ) )
        # time.sleep(1)
        photo = web_scraper.get_photo('http://localhost:8000/index.html', saveLoc)
        httpd.server_close()
        return photo

    def evaluate_photo(self) -> float:
        photo = self.gen_photo()
        # TODO: Evaluate a photo based on some criteria
        return 1

    def evaluate_css(self) -> float:
        return self.css.evaluate()

    def evaluate(self) -> float:
        css_evaluation = self.evaluate_css()
        # TODO: Actually evaluate a site so that we don't get index errors in MCTS
        return random.random()
        if css_evaluation < WebPage.css_eval_limit:
            return 0
        else:
            photo_evaluation = self.evaluate_photo()
            return css_evaluation*.2 + photo_evaluation*.8

    def __str__(self):
        return str((self.html, self.css))

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memo): #Pass a reference to the original HTML but create a copy of the css 
        ws = WebPage(html=self.html)
        # print("here")
        ws.css = deepcopy(self.css)
        return ws


def run_server(server):
    server.serve_forever()

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return