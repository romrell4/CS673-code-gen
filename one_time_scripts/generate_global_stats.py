import json
import os
from typing import Tuple

from bs4 import BeautifulSoup
from tqdm import tqdm

from webscraping.dao import Dao, Rule, Tag
from webscraping.stat_models import CSS, GlobalStats
from webscraping.web_scraper import scraper

class StatGenerator:
    def __init__(self):
        self.data = GlobalStats.read()
        self.soups = None
        self.dao = Dao()

    def get_soups(self, limit = None, test_only = False) -> [Tuple[str, BeautifulSoup]]:
        if self.soups is None:
            if test_only:
                dir_names = ["test"]
            else:
                dir_names = os.listdir("../cached_sites")
                if limit is not None:
                    dir_names = dir_names[:limit]
            self.soups = []
            for dir_name in tqdm(dir_names, desc = "Scraping soups"):
                # print(dir_name)
                self.soups.append((dir_name, scraper.get_soup(dir_name)))
        return self.soups

    def write(self, filename = GlobalStats.DEFAULT_FILENAME):
        with open(filename, "w") as f:
            json.dump(self.data, f, indent = 2)

    def add_tags_to_db(self):
        self.dao.flush_tags()

        tags: [Tag] = []
        for web_page, soup in tqdm(self.get_soups()):
            for tag in soup.find_all():
                tags.append(Tag(None, web_page, tag.name, tag.get("id"), ",".join(tag.get("class", []))))
        self.dao.add_tags(tags)

    def add_rules_to_db(self):
        self.dao.flush_rules()

        rules: [Rule] = []
        for web_page, soup in tqdm(self.get_soups(), desc = "Gathering rules"):
            css = CSS(soup)
            for selector, rule_set in css.selectors.items():
                for key, value in rule_set.items():
                    rules.append(Rule(None, web_page, selector, key, value))
        self.dao.add_rules(rules)


def generate():
    generator = StatGenerator()
    # generator.add_rules_to_db()
    generator.add_tags_to_db()
    generator.write()


if __name__ == '__main__':
    generate()
