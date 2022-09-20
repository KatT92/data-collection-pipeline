from logging import error
from pyclbr import Function
from urllib.error import URLError
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import config


class LinkScraper:

    def __init__(self, bgg_url):
        options = Options()
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        self.URL = bgg_url
        self.links = []
        self.driver.get(self.URL)  # initial url

    def goToPage(self, i):
        print('i', i)
        if i <= 100:
            self.driver.get(self.URL)
        elif i > 100:
            page_number = int(i/100) + 1
            self.driver.get(self.URL + str(page_number))

    def bypassCookies(self):
        try:
            # This is the id of the frame
            accept_cookies_button = self.driver.find_element(
                by=By.XPATH, value='//*[@id="c-p-bn"]')
            accept_cookies_button.click()

        except AttributeError:  # If you have the latest version of Selenium, the code above won't run because the "switch_to_frame" is deprecated
            # This is the id of the frame
            accept_cookies_button = self.driver.find_element(
                by=By.XPATH, value='//*[@id="c-p-bn"]')  # div id = c-bns, c-p-bn
            accept_cookies_button.click()

        except:
            pass  # If there is no cookies button, we won't find it, so we can pass
        pass

    def getLinks(self, i):
        if i % 100 != 0:
            j = i % 100
        else:
            j = i
        print('i, j', i, j)

        game_property = self.driver.find_element(
            by=By.XPATH, value=f'//*[@id="results_objectname{j}"]')
        a_tag = game_property.find_element(by=By.TAG_NAME, value='a')
        link = a_tag.get_attribute('href')
        self.links.append(link)
        time.sleep(2)

    def createLinksFile(self):
        print(self.links)
        file = open("bg_links.py", "w")
        file.write(f'links = {self.links}')
        file.close()


def getInfo(urllist):
    info = LinkScraper(urllist)
    time.sleep(2)
    info.bypassCookies()
    time.sleep(2)

    print('insert min number')
    temp = input()
    try:
        init_number = int(temp)
    except:
        init_number = 0  # initialise

    while init_number < 1 or type(init_number) != int:
        print('try again')
        try:
            init_number = int(input())
        except:
            pass

    print('insert max number')
    temp = input()
    try:
        max_number = int(temp)
    except:
        max_number = 0  # initialise

    while max_number <= init_number or type(max_number) != int:
        print('try again')
        try:
            max_number = int(input())
        except:
            pass

    # make sure you get ranks for pages we need them from
    for i in range(init_number, max_number):
        if i == init_number or (i-1) % 100 == 0:
            info.goToPage(i)
        info.getLinks(i)
    info.createLinksFile()


if __name__ == "__main__":
    bgg_url = config.url
    getInfo(bgg_url)
    time.sleep(2)
    print('exit')
