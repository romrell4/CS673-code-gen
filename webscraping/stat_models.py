from typing import Tuple

import tinycss2
from bs4 import BeautifulSoup

from webscraping import web_scraper

class HTML:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
        all_tags = soup.find_all()
        self.tags = set([tag.name for tag in all_tags])
        self.ids = set([tag["id"] for tag in all_tags if tag.get("id") is not None])
        self.classes = set([klass for tag in all_tags if tag.get("class") is not None for klass in tag["class"]])

class CSS:
    def __init__(self, html_soup: BeautifulSoup, print_issues = False):
        self.print_issues = print_issues
        self.rule_sets = {}
        for style in html_soup.find_all("style"):
            stylesheet = tinycss2.parse_stylesheet(style.text, skip_comments = True, skip_whitespace = True)
            for rule_set in stylesheet:
                # If the prelude contains a comma, there are multiple selectors
                for selector in tinycss2.serialize(rule_set.prelude).split(","):
                    selector = selector.strip()
                    if selector not in self.rule_sets:
                        self.rule_sets[selector] = {}
                    # Update the current dictionary, overwriting conflicting keys
                    self.rule_sets[selector].update({declaration.lower_name: tinycss2.serialize(declaration.value).strip() for declaration in tinycss2.parse_declaration_list(rule_set.content, skip_comments = True, skip_whitespace = True)})

class WebPage:
    def __init__(self, url: str):
        soup = web_scraper.get_soup(url)
        self.html = HTML(soup)
        self.css = CSS(soup)

    def generate_web_page(self) -> Tuple[str, str]:
        # TODO: Implement this
        pass