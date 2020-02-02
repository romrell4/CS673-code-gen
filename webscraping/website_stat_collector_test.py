import unittest
from webscraping.stat_models import *
from webscraping import web_scraper

class StatCollectionTest(unittest.TestCase):
    def test_html(self):
        html = HTML(web_scraper.get_soup("test"))
        self.assertCountEqual(html.tags, ["html", "head", "title", "style", "body", "div", "h1", "p", "span", "table", "thead", "tr", "th", "tbody", "td", "img", "button"])
        self.assertCountEqual(html.ids, ["content", "title", "test-table", "awesomeBtn"])
        self.assertCountEqual(html.classes, ["center", "red", "image", "icon", "blue", "big"])

    def full_test(self):
        web_page = WebPage.from_url("test")
        self.assertIsInstance(web_page, WebPage)
        self.assertIsNotNone(web_page.html.soup)
        self.assertCountEqual(web_page.html.tags, ["html", "head", "title", "style", "body", "div", "h1", "p", "table", "thead", "tr", "th", "tbody", "td", "img", "button"])
        self.assertCountEqual(web_page.html.ids, ["content", "title", "test-table", "awesomeBtn"])
        self.assertCountEqual(web_page.html.classes, ["center", "red", "image", "icon", "blue", "big"])


if __name__ == '__main__':
    unittest.main()
