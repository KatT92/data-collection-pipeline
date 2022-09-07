from logging import error
from pyclbr import Function
from urllib.error import URLError
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from decouple import config


class Scraper:

    def __init__(self, url):
        options = Options()
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        self.URL = url
        self.driver.get(self.URL)
        self.links = []

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
        game_property = self.driver.find_element(
            by=By.XPATH, value=f'//*[@id="results_objectname{i}"]')
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
    info = Scraper(urllist)
    time.sleep(2)
    info.bypassCookies()
    time.sleep(2)
    for i in range(1, 10):
        info.getLinks(i)
    info.createLinksFile()


if __name__ == "__main__":
    url = config('URL')
    print(url)
    getInfo(url)
    time.sleep(2)
    print('exit')
