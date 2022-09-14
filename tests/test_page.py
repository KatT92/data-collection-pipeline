from pageScraper import PageScraper
import unittest
from bg_links import links as urllist


class PageScraperTestCase(unittest.TestCase):
    def test_len_links(self):
        scraper = PageScraper(urllist)
        scraper.driver.get(urllist[0])
        scraper.getPageData()
        actual_value = scraper.data['game_name']
        print(actual_value)
        expected_value = 'Gloomhaven'
        self.assertEqual(expected_value, actual_value)
        print('test page')
        scraper.driver.quit()


unittest.main(argv=[''], verbosity=0, exit=False)

if __name__ == '__main__':
    unittest.main()
