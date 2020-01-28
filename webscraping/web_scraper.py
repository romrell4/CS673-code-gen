from bs4 import BeautifulSoup
import requests
import sys
import time
import tinycss2

def running_linux():
    return 'linux' in sys.platform

def scrape(url):
    html = get_html(url)
    get_photo(url)
    soup = BeautifulSoup(html, "html.parser")
    all_css_rules = []
    for styles in soup.select('style'):
        # print(styles)
        css = tinycss2.parse_stylesheet(styles.contents[0], skip_comments=True,skip_whitespace=True)
        # print(css)
        for rule in css:
            all_css_rules.append(rule)
    return soup, all_css_rules

def get_photo(url):
    if url.startswith("http") and running_linux():
        import dryscrape
        session = dryscrape.Session()
        session.visit(url)
        time.sleep(1)
        session.render(f"{url}.png")
        return

def get_html(url):
    """
    Either read the element from a live website, or a local html file - depending on the prefix

    :param url: Either a remote of local url to an html file
    :return: html text
    """
    if url.startswith("http"):
        if running_linux():
            import dryscrape
            session = dryscrape.Session()
            session.visit(url)
            return session.body()
        else:
            return requests.get(url).text
    else:
        with open("test_html/" + url) as f:
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
    if running_linux():
        import dryscrape

        # start xvfb in case no X is running. Make sure xvfb
        # is installed, otherwise this won't work!
        dryscrape.start_xvfb()

    # scrape("https://www.crummy.com/software/BeautifulSoup/bs4/doc/")
    # scrape("https://recipes.twhiting.org")
    # soup, _ = scrape("test.html")
    soup, _ = scrape("https://byu.edu")

    # print(soup.prettify())
    all_tags = parse_children(soup.body, print_structure = True)
    # [print(tag) for tag in all_tags]
