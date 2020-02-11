import argparse
from copy import deepcopy, copy
from typing import List, Iterable

import tinycss2
from bs4 import BeautifulSoup
from tinycss2.ast import ParseError

from webscraping.dao import Dao, ValueCount
from webscraping.web_scraper import scraper

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
            self.soup = scraper.get_soup(url)
        else:
            self.soup = soup
        all_tags = soup.find_all()
        self.tags = set([tag.name for tag in all_tags])
        self.ids = set([tag["id"] for tag in all_tags if tag.get("id") is not None])
        self.classes = set([klass for tag in all_tags if tag.get("class") is not None for klass in tag["class"]])

    def containsSelector(self, selector):
        if selector in self.tags:
            # print(f"Selector {selector} in tags")
            return True
        if selector in self.ids:
            # print(f"Selector {selector} in ids")
            return True
        if selector in self.classes:
            # print(f"Selector {selector} in classes")
            return True
        return False

class CSS:
    """
    Class used to represent the style of a web page

    Attributes:
        selectors ([str: [str: str]): dictionary of selector (e.g. "thead" or "p#some-id") to the key-value pairs of rules (e.g. "font-size": "18pt")
    """

    def __init__(self, html_soup: BeautifulSoup = None, print_issues = False, url: str = None):
        if url is not None:
            html_soup = scraper.get_soup(url)
        self.print_issues = print_issues
        self.selectors = {}
        for style in html_soup.find_all("style"):
            stylesheet = tinycss2.parse_stylesheet(style.text, skip_comments = True, skip_whitespace = True)
            for rule_set in [rule_set for rule_set in stylesheet if type(rule_set) != ParseError]:
                if rule_set.type in ("error", "at-rule"):
                    continue
                # If the prelude contains a comma, there are multiple selectors
                for selector in tinycss2.serialize(rule_set.prelude).split(","):
                    selector = selector.strip()
                    if selector not in self.selectors:
                        self.selectors[selector] = {}
                    # Update the current dictionary, overwriting conflicting keys
                    declarations = tinycss2.parse_declaration_list(rule_set.content, skip_comments = True, skip_whitespace = True)
                    self.selectors[selector].update({declaration.lower_name: tinycss2.serialize(declaration.value).strip() for declaration in declarations if declaration.type not in ("error", "at-rule")})

    def containsSelector(self, selector):
        return selector in self.selectors.keys()

    def evaluate(self):
        # TODO: Actually evaluate the quality of CSS based on global stats or some metrics
        return 1

    def generate_css(self) -> str:
        rules = ""
        for k, v in self.selectors.items():
            rules += f"{k} {v}\n"
        return rules

    def addRule(self, selector, rule_name, rule_value):
        if selector not in self.selectors:
            self.selectors[selector] = {}
        self.selectors[selector].update({rule_name: rule_value})

class WebPage:
    """
    Class used to represent a web page

    Attributes:
        html (HTML): info about the HTML of the web page
        css (CSS): info about the CSS of the web page
    """
    photo_eval_limit = .2
    css_eval_limit = .7

    def __init__(self, url = None, html = None):
        if url is not None:
            soup = scraper.get_soup(url)
            self.html = HTML(soup)
            self.css = CSS(soup)
        elif html is not None:
            self.html = html
            self.css = None
        else:
            raise argparse.ArgumentError(self, "Invalid Arguments for creating a WebPage")

    def containsSelector(self, selector):
        return self.html.containsSelector(selector) or self.css.containsSelector(selector)

    def generate_web_page(self) -> bytes:
        webpageSoup = copy(self.html.soup)
        style_tag = webpageSoup.new_tag('style')
        style_tag.string = self.css.generate_css()
        try:
            webpageSoup.head.insert(0, style_tag)
        except:
            webpageSoup.insert(0, webpageSoup.new_tag('head'))
            webpageSoup.head.insert(0, style_tag)
        return webpageSoup.encode()

    def gen_photo(self, saveLoc = "screenshot.png"):
        photo = None
        with open("index.html", 'wb+') as indexFile:
            indexFile.write(self.generate_web_page())
            indexFile.flush()
        scraper.get_photo("http://localhost:8000/index.html", saveLoc = saveLoc)
        # os.remove("index.html")
        return photo

    def evaluate_photo(self):
        photo = self.gen_photo()
        # TODO: Evaluate a photo based on some criteria
        return 1

    def evaluate_css(self):
        return self.css.evaluate()

    def evaluate(self):
        css_evaluation = self.evaluate_css()
        # TODO: Actually evaluate a site so that we don't get index errors in MCTS
        return 1
        if css_evaluation < WebPage.css_eval_limit:
            return 0
        else:
            photo_evaluation = self.evaluate_photo()
            return css_evaluation * .2 + photo_evaluation * .8

    def __str__(self):
        return str((self.html, self.css))

    def __repr__(self):
        return str(self)

    def __deepcopy__(self, memo):  # Pass a reference to the original HTML but create a copy of the css
        ws = WebPage(html = self.html)
        # print("here")
        ws.css = deepcopy(self.css)
        return ws

class GlobalStats:
    def __init__(self):
        dao = Dao()

        self.rule_key_counts = dao.get_rule_key_counts()
        self.rule_key_counts_tuple = self.convert_to_lists(self.rule_key_counts)
        self.rule_key_value_counts = dao.get_rule_values_by_rule_key()
        self.tag_counts = dao.get_tag_counts()
        self.tag_rule_key_counts = dao.get_tag_rule_key_counts()

    @staticmethod
    def convert_to_lists(value_counts: List[ValueCount]) -> Iterable[List]:
        return map(list, zip(*[(value_count.value, value_count.count) for value_count in value_counts]))

    def __deepcopy__(self, memo):
        return self
