import sys

import tinycss2
from bs4 import BeautifulSoup
# Need to install the webdriver https://sites.google.com/a/chromium.org/chromedriver/home
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium.webdriver.common.keys import Keys
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
        self.width = 0
        self.height = 0
        self.set_long_mobile_view()
        self.chrome_options = Options()
        if running_linux():
            self.chrome_options.binary_location = "/usr/bin/google-chrome-stable"
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument("--incognito")
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.set_window_size()
        self.waitTime = 1
        self.httpd = HTTPServer(('',8000), CustomHTTPRequestHandler)
        self.thd = _thread.start_new_thread(run_server, (self.httpd, ) )
        # time.sleep(1)
        # httpd.server_close()

    def set_desktop_view(self):
        self.width = 1024
        self.height = 800

    def set_mobile_view(self):
        self.width = 600
        self.height = 800

    def set_long_mobile_view(self):
        self.width = 600
        self.height = 1500

    def set_window_size(self):
        self.driver.set_window_size(self.width, self.height)

    def restart_selenium(self, full_restart=False):
        # print("restarting selenium")
        if full_restart:
            self.driver.quit()
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.set_window_size()

        send_command = ('POST', '/session/$sessionId/chromium/send_command')
        self.driver.command_executor._commands['SEND_COMMAND'] = send_command
        self.driver.execute('SEND_COMMAND', dict(cmd='Network.clearBrowserCache', params={}))
        # self.driver.find_element_by_css_selector("* /deep/ #clearBrowsingDataConfirm").send_keys(Keys.ENTER)

    def get_soup(self, url, cached_site_dir="../resources/cached_sites", cleaned=False):
        return BeautifulSoup(self.get_html(url, cached_site_dir, cleaned), "html.parser")

    def scrape(self, url, cleaned: bool = False):
        soup: BeautifulSoup = self.get_soup(url, cleaned=cleaned)
        self.get_photo(url)
        all_css_rules = []
        for styles in soup.select('style'):
            # print(styles)
            css = tinycss2.parse_stylesheet(styles.contents[0], skip_comments=True,skip_whitespace=True)
            # print(css)
            for rule in css:
                all_css_rules.append(rule)
        return soup, all_css_rules

    def get_photo(self, url, save_loc: str = "screenshot.png"):
        if "localhost" in url:
            # TODO: Make sure that the selenium cache is reset between visits
            self.restart_selenium()
        self.driver.get(url)
        wait = WebDriverWait(self.driver, self.waitTime)
        self.driver.save_screenshot(save_loc)
        return save_loc

    def get_html(self, url: str, cached_site_dir: str, cleaned: bool = False):
        """
        Either read the element from a live website, or a local html file - depending on the prefix

        :param url: Either a full website url or folder name for one of the cached sites
        :param cached_site_dir: the directory where the cached sites are stored. No trailing "/"
        :param cleaned whether to get the cleaned site or not
        :return: html text
        """
        if url.startswith("http"):
            self.driver.get(url)
            wait = WebDriverWait(self.driver, self.waitTime)
            return self.driver.page_source
        else:
            if cleaned:
                with open("{}/{}/cleaned.html".format(cached_site_dir, url)) as f:
                    return f.read()
            else:
                with open("{}/{}/combined.html".format(cached_site_dir, url)) as f:
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
    all_tags = scraper.parse_children(soup.body, print_structure=True)
    # [print(tag) for tag in all_tags]
