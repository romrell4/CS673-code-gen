import unittest
from webscraping import website_stat_collector

class MyTestCase(unittest.TestCase):
    def test_simple(self):
        stats = website_stat_collector.parse_website("test")
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
