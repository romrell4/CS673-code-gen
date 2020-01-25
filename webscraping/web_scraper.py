from bs4 import BeautifulSoup
import requests
import sys
import time

def running_linux():
    return 'linux' in sys.platform

def scrape(url):
    html = get_html(url)
    get_photo(url)
    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    all_tags = parse_children(soup.body, 0)
    #[print(tag) for tag in all_tags]
    return soup

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

def parse_children(tag, depth):
    """
    Here's one simple way to parse the dom recursively, in a depth first fashion.
    :param tag: Any bs4 tag
    :param depth: The current depth in our DFS
    """
    tags = []
    for child in tag.children:
        if child.name is not None:
            tags.append(Tag(child))
            #print("{}{}".format("  " * depth, child.name))
            tags += parse_children(child, depth + 1)
    return tags

class Tag:
    def __init__(self, bs4_tag):
        self.id = bs4_tag.get("id")
        self.classes = bs4_tag.get("class")
        self.name = bs4_tag.name
        self.bs4_tag = bs4_tag

    def __str__(self):
        return "Tag(name: {}, id: {}, classes: {})".format(self.name, self.id, self.classes)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    if running_linux():
        import dryscrape

        # start xvfb in case no X is running. Make sure xvfb
        # is installed, otherwise this won't work!
        dryscrape.start_xvfb()

    # scrape("https://www.crummy.com/software/BeautifulSoup/bs4/doc/")
    scrape("test.html")
