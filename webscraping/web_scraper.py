import sys

import tinycss2
from bs4 import BeautifulSoup
# Need to install the webdriver https://sites.google.com/a/chromium.org/chromedriver/home
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def running_linux():
    return 'linux' in sys.platform

def get_soup(url):
    return BeautifulSoup(get_html(url), "html.parser")

def scrape(url):
    soup = get_soup(url)
    get_photo(url)
    all_css_rules = []
    for styles in soup.select('style'):
        # print(styles)
        css = tinycss2.parse_stylesheet(styles.contents[0], skip_comments=True,skip_whitespace=True)
        # print(css)
        for rule in css:
            all_css_rules.append(rule)
    return soup, all_css_rules

def get_photo(url, saveLoc="screenshot.png"):
    chrome_options = Options()
    if running_linux():
        chrome_options.binary_location = "/usr/bin/google-chrome-stable"
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.set_window_size(1080,800)
        driver.get(url)
        wait = WebDriverWait(driver, 1)
        driver.save_screenshot(saveLoc)
    return saveLoc

def get_html(url):
    """
    Either read the element from a live website, or a local html file - depending on the prefix

    :param url: Either a full website url or folder name for one of the cached sites
    :return: html text
    """
    if url.startswith("http"):
        chrome_options = Options()
        if running_linux():
            chrome_options.binary_location = "/usr/bin/google-chrome-stable"
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        with webdriver.Chrome(options=chrome_options) as driver:
            driver.set_window_size(1080,800)
            driver.get(url)
            wait = WebDriverWait(driver, 1)
            return driver.page_source
    else:
        with open("../cached_sites/{}/combined.html".format(url)) as f:
            return f.read()

def parse_children(tag, depth = 0, print_structure = False):
    """
    Here's one simple way to parse the dom recursively, in a depth first fashion.
    :param tag: Any bs4 tag
    :param depth: The current depth in our DFS
    :param print_structure: whether or not to print the tree as we go
    """
    tags = []
    for child in tag.children:
        if child.name is not None:
            tags.append(Tag(child))
            if print_structure:
                print("{}{}".format("  " * depth, child.name))
            tags += parse_children(child, depth + 1, print_structure)
    return tags

class Tag:
    def __init__(self, bs4_tag):
        self.id = bs4_tag.get("id")
        self.classes = bs4_tag.get("class", [])
        self.name = bs4_tag.name
        self.bs4_tag = bs4_tag

    def __str__(self):
        return "Tag(name: {}, id: {}, classes: {})".format(self.name, self.id, self.classes)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return isinstance(other, Tag) and self.id == other.id and self.classes == other.classes and self.name == other.name


if __name__ == '__main__':
    # scrape("https://www.crummy.com/software/BeautifulSoup/bs4/doc/")
    # scrape("https://recipes.twhiting.org")
    # soup, _ = scrape("test")
    soup, _ = scrape("https://byu.edu")

    # print(soup.prettify())
    all_tags = parse_children(soup.body, print_structure = True)
    # [print(tag) for tag in all_tags]
