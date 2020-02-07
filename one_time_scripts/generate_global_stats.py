import json
import os
import tinycss2
from tqdm import tqdm
from webscraping.web_scraper import scraper
from webscraping.stat_models import CSS

class Stats:
    DEFAULT_FILENAME = "../resources/global_stats.json"

    def __init__(self, data):
        self.data = data
        self.soups = None
        if data is not None:
            self.rule_names = list(data["known_rule_values"].keys())
            self.rule_freqs = list()
            for rule_value in data["known_rule_values"].values():
                num_items = 0
                for value in rule_value.values():
                    num_items += 1
                self.rule_freqs.append(num_items)
            self.rule_values = data["known_rule_values"]
            self.selectors = list(data['tag_freq'].keys())
            self.selector_freq = list(data["tag_freq"].values())

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

    @staticmethod
    def read(filename = DEFAULT_FILENAME):
        with open(filename) as f:
            return Stats(json.load(f))

    def write(self, filename = DEFAULT_FILENAME):
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
    
    def __deepcopy__(self, memo):
        return self


def generate():
    stats = Stats.read()
    # stats.calc_tag_freq()
    stats.calc_possible_rule_values()
    stats.write()


if __name__ == '__main__':
    generate()
