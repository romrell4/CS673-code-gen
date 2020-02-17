import unittest

from webscraping.stat_models import CSS
from webscraping.web_scraper import scraper

class CssEvaluatorTest(unittest.TestCase):
    def test_color_evaluation(self):
        css = CSS(scraper.get_soup("byu"))
        css.evaluate_colors()


if __name__ == '__main__':
    unittest.main()
