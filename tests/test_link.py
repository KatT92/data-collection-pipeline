from linkScraper import LinkScraper
import unittest
from decouple import config


class LinkScraperTestCase(unittest.TestCase):
    def test_len_links(self):
        url = config('URL')
        scraper = LinkScraper(url)
        scraper.getLinks(1)
        actual_value = scraper.links[0]
        expected_value = 'https://boardgamegeek.com/boardgame/174430/gloomhaven'
        self.assertEqual(expected_value, actual_value)
        print('test links')
        scraper.driver.quit()


unittest.main(argv=[''], verbosity=0, exit=False)

if __name__ == '__main__':
    unittest.main()
