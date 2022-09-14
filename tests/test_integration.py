from linkScraper import LinkScraper
from pageScraper import PageScraper
import unittest
from decouple import config


class IntegrationTestCase(unittest.TestCase):
    def test_links(self):
        url = config('URL')
        scraper1 = LinkScraper(url)
        scraper1.getLinks(1)
        urllist = scraper1.links
        scraper2 = PageScraper(urllist)
        scraper2.driver.get(urllist[0])
        scraper2.getPageData()
        actual_value = scraper2.data['game_name']
        print(actual_value)
        expected_value = 'Gloomhaven'
        self.assertEqual(expected_value, actual_value)
        scraper1.driver.quit()
        scraper2.driver.quit()


unittest.main(argv=[''], verbosity=0, exit=False)

if __name__ == '__main__':
    unittest.main()
