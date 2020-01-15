from bs4 import BeautifulSoup
import requests

def scrape(url):
    html = get_html(url)

    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    parse_children(soup.body, 0)

def get_html(url):
    """
    Either read the element from a live website, or a local html file - depending on the prefix

    :param url: Either a remote of local url to an html file
    :return: html text
    """
    if url.startswith("http"):
        return requests.get(url).text
    else:
        with open(url) as f:
            return f.read()

def parse_children(element, depth):
    """
    Here's one simple way to parse the dom recursively, in a depth first fashion.
    :param element: Any bs4 element
    :param depth: The current depth in our DFS
    """
    for child in element.children:
        if child.name is not None:
            print("{}{}".format("  " * depth, child.name))
            parse_children(child, depth + 1)

if __name__ == '__main__':
    # scrape("https://www.crummy.com/software/BeautifulSoup/bs4/doc/")
    scrape("webscraping/test.html")