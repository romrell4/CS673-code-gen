from typing import Tuple

from bs4 import BeautifulSoup

class HTML:
    def __init__(self, soup: BeautifulSoup, tags: [str], ids: [str], classes: [str]):
        self.soup = soup
        self.tags = tags
        self.ids = ids
        self.classes = classes

class Rule:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

class RuleSet:
    def __init__(self, selector: str, rules: [Rule]):
        self.selector = selector
        self.rules = rules

class CSS:
    def __init__(self, rule_sets: [RuleSet]):
        self.rule_sets = rule_sets

class WebPage:
    def __init__(self, html: HTML, css: CSS):
        self.html = html
        self.css = css

    def generate_web_page(self) -> Tuple[str, str]:
        # TODO: Implement this
        pass