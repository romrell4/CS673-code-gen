import sys

import tinycss2
from bs4 import BeautifulSoup
# Need to install the webdriver https://sites.google.com/a/chromium.org/chromedriver/home
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from http.server import HTTPServer, SimpleHTTPRequestHandler
import _thread

def running_linux():
    return 'linux' in sys.platform

def run_server(server):
    server.serve_forever()

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

class WebScraper:
    def __init__(self):
        self.chrome_options = Options()
        if running_linux():
            self.chrome_options.binary_location = "/usr/bin/google-chrome-stable"
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.set_window_size(1080,800)
        self.waitTime = 1
        self.httpd = HTTPServer(('',8000), CustomHTTPRequestHandler)
        self.thd = _thread.start_new_thread(run_server, (self.httpd, ) )
        # time.sleep(1)
        # httpd.server_close()

    def get_soup(self, url):
        return BeautifulSoup(self.get_html(url), "html.parser")

    def scrape(self, url):
        soup = self.get_soup(url)
        self.get_photo(url)
        all_css_rules = []
        for styles in soup.select('style'):
            # print(styles)
            css = tinycss2.parse_stylesheet(styles.contents[0], skip_comments=True,skip_whitespace=True)
            # print(css)
            for rule in css:
                all_css_rules.append(rule)
        return soup, all_css_rules

    def get_photo(self, url, saveLoc="screenshot.png"):
        self.driver.get(url)
        wait = WebDriverWait(self.driver, self.waitTime)
        self.driver.save_screenshot(saveLoc)
        return saveLoc

    def get_html(self, url):
        """
        Either read the element from a live website, or a local html file - depending on the prefix

        :param url: Either a full website url or folder name for one of the cached sites
        :return: html text
        """
        if url.startswith("http"):
            self.driver.get(url)
            wait = WebDriverWait(self.driver, self.waitTime)
            return self.driver.page_source
        else:
            with open("../cached_sites/{}/combined.html".format(url)) as f:
                return f.read()

    def parse_children(self, tag, depth = 0, print_structure = False):
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
                tags += self.parse_children(child, depth + 1, print_structure)
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

scraper = WebScraper()


if __name__ == '__main__':
    # scrape("https://www.crummy.com/software/BeautifulSoup/bs4/doc/")
    # scrape("https://recipes.twhiting.org")
    # soup, _ = scrape("test")
   
    soup, _ = scraper.scrape("https://byu.edu")

    # print(soup.prettify())
    all_tags = scraper.parse_children(soup.body, print_structure = True)
    # [print(tag) for tag in all_tags]
