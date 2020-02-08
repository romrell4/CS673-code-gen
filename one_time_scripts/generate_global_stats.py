import json
import os

from tqdm import tqdm

from webscraping.stat_models import CSS, GlobalStats
from webscraping.web_scraper import scraper

class StatGenerator:
    def __init__(self):
        self.data = GlobalStats.read()
        self.soups = None

    def get_soups(self, limit = None, test_only = False):
        if self.soups is None:
            print("Scraping soups...")
            if test_only:
                dir_names = ["test"]
            else:
                dir_names = os.listdir("../cached_sites")
                if limit is not None:
                    dir_names = dir_names[:limit]
            self.soups = []
            for dir_name in tqdm(dir_names):
                # print(dir_name)
                self.soups.append(scraper.get_soup(dir_name))
        return self.soups

    def write(self, filename = GlobalStats.DEFAULT_FILENAME):
        with open(filename, "w") as f:
            json.dump(self.data, f, indent = 2)

    def calc_tag_freq(self):
        tag_freq = {}
        for soup in tqdm(self.get_soups()):
            for tag in soup.find_all():
                tag_name = tag.name
                if tag_name not in tag_freq:
                    tag_freq[tag_name] = 0
                tag_freq[tag_name] += 1
        self.data["tag_freq"] = tag_freq

    def calc_possible_rule_values(self):
        rules = {}
        for soup in self.get_soups():
            css = CSS(soup)
            for rule_set in css.selectors.values():
                for key, value in rule_set.items():
                    if key not in rules:
                        rules[key] = {}
                    if value not in rules[key]:
                        rules[key][value] = 0
                    rules[key][value] += 1

        self.data["known_rule_values"] = rules


def generate():
    generator = StatGenerator()
    generator.calc_tag_freq()
    # stats.calc_possible_rule_values()
    generator.write()


if __name__ == '__main__':
    generate()
