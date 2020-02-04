import json
import os
import tinycss2
from tqdm import tqdm
from webscraping import web_scraper
from webscraping.stat_models import CSS

class Stats:
    DEFAULT_FILENAME = "../resources/global_stats.json"

    def __init__(self, data):
        self.data = data
        self.soups = None

    def get_soups(self, limit = None):
        if self.soups is None:
            print("Scraping soups...")
            dir_names = os.listdir("../cached_sites")
            if limit is not None:
                dir_names = dir_names[:limit]
            self.soups = [web_scraper.get_soup(dir_name) for dir_name in tqdm(dir_names)]
        return self.soups

    @staticmethod
    def read(filename = DEFAULT_FILENAME):
        with open(filename) as f:
            return Stats(json.load(f))

    def write(self, filename = DEFAULT_FILENAME):
        with open(filename, "w") as f:
            json.dump(self.data, f)

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
        for soup in tqdm(self.get_soups(limit = 10)):
            CSS(soup)

        self.data["known_rule_values"] = rules



def generate():
    stats = Stats.read()
    # stats.calc_tag_freq()
    stats.calc_possible_rule_values()
    stats.write()


if __name__ == '__main__':
    generate()
