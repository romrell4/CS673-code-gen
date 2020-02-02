import json
import os
from tqdm import tqdm
from webscraping import web_scraper

class Stats:
    DEFAULT_FILENAME = "../resources/global_stats.json"

    def __init__(self, data):
        self.data = data

    @staticmethod
    def read(filename = DEFAULT_FILENAME):
        with open(filename) as f:
            return Stats(json.load(f))

    def write(self, filename = DEFAULT_FILENAME):
        with open(filename, "w") as f:
            json.dump(self.data, f)

    def calc_tag_freq(self):
        tag_freq = {}
        for directory in tqdm(os.listdir("../cached_sites")):
            soup = web_scraper.get_soup(directory)
            for tag in soup.find_all():
                tag_name = tag.name
                if tag_name not in tag_freq:
                    tag_freq[tag_name] = 0
                tag_freq[tag_name] += 1
        self.data["tag_freq"] = tag_freq

def generate():
    stats = Stats.read()
    # stats.calc_tag_freq()
    stats.write()


if __name__ == '__main__':
    generate()
