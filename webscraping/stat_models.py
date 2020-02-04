from typing import Tuple

import tinycss2
from bs4 import BeautifulSoup
from tinycss2.ast import ParseError

from webscraping import web_scraper

class HTML:
    """
    Class used to represent the DOM of a web page

    Attributes:
        soup (BeautifulSoup): the soup containing the parsed HTML
        tags ([str]): all unique tags used on the web page
        ids ([str]): all unique ids used on the web page
        classes ([str]): all unique classes used on the web page
    """

    def __init__(self, soup: BeautifulSoup):
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

    def __init__(self, html_soup: BeautifulSoup, print_issues = False):
        self.print_issues = print_issues
        self.selectors = {}
        for style in html_soup.find_all("style"):
            stylesheet = tinycss2.parse_stylesheet(style.text, skip_comments = True, skip_whitespace = True)
            for rule_set in [rule_set for rule_set in stylesheet if type(rule_set) != ParseError]:
                # If the prelude contains a comma, there are multiple selectors
                for selector in tinycss2.serialize(rule_set.prelude).split(","):
                    selector = selector.strip()
                    if selector not in self.selectors:
                        self.selectors[selector] = {}
                    # Update the current dictionary, overwriting conflicting keys
                    declarations = tinycss2.parse_declaration_list(rule_set.content, skip_comments = True, skip_whitespace = True)
                    self.selectors[selector].update({declaration.lower_name: tinycss2.serialize(declaration.value).strip() for declaration in declarations if type(declaration) != ParseError})

class WebPage:
    """
    Class used to represent a web page

    Attributes:
        html (HTML): info about the HTML of the web page
        css (CSS): info about the CSS of the web page
    """

    def __init__(self, url: str):
        soup = web_scraper.get_soup(url)
        self.html = HTML(soup)
        self.css = CSS(soup)

    def generate_web_page(self) -> Tuple[str, str]:
        # TODO: Implement this
        pass
