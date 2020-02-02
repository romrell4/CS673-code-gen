import unittest
from webscraping.stat_models import *
from webscraping import web_scraper

class StatCollectionTest(unittest.TestCase):
    def test_html(self):
        html = HTML(web_scraper.get_soup("test"))
        self.assertCountEqual(html.tags, ["html", "head", "title", "style", "body", "div", "h1", "p", "span", "table", "thead", "tr", "th", "tbody", "td", "img", "button"])
        self.assertCountEqual(html.ids, ["content", "title", "test-table", "awesomeBtn"])
        self.assertCountEqual(html.classes, ["center", "red", "image", "icon", "blue", "big"])

    def test_css(self):
        css = CSS(web_scraper.get_soup("test"), True)
        self.assertCountEqual(css.rule_sets, ["body", "#content", "#title", "p", ".center", ".red", ".blue", ".big", "table#test-table", "td.image", "img.icon", "th, td"])
        self.assertEqual(css.rule_sets["body"], {
            "font-size": "18pt",
            "background-image": "url(\"https://www.ezoic.com/wp-content/uploads/2016/05/website-background-min.jpg\")",
            "background-repeat": "no-repeat"
        })
        self.assertEqual(css.rule_sets["#content"], {
            "width": "50%",
            "background-color": "#dddddddd",
            "padding": "20px"
        })

    def test_full_web_page(self):
        web_page = WebPage("test")
        self.assertIsInstance(web_page, WebPage)
        self.assertIsNotNone(web_page.html.soup)
        self.assertCountEqual(web_page.html.tags, ["html", "head", "title", "style", "body", "div", "h1", "p", "table", "thead", "tr", "th", "tbody", "td", "img", "button"])
        self.assertCountEqual(web_page.html.ids, ["content", "title", "test-table", "awesomeBtn"])
        self.assertCountEqual(web_page.html.classes, ["center", "red", "image", "icon", "blue", "big"])


if __name__ == '__main__':
    unittest.main()
