import os
import urllib.request
import uuid  # uuid4
from time import sleep
from bg_links import links
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# from logging import error
# from pyclbr import Function
# from turtle import ScrolledCanvas, position
# from urllib.error import URLError


class PageScraper:

    def __init__(self, urllist):
        options = Options()
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        self.data = ""
        self.images = []
        self.cwd = os.getcwd()
        self.urllist = urllist

    # def goToPage(self, j):
    #     self.URL = self.urllist[j]
    #     self.target_dir = self.cwd + '/raw_data' + '/' + self.URL.split("/")[4]

    def goToPage(self, j):
        self.URL = self.urllist[j]
        self.target_dir = self.cwd + \
            '/raw_data/' + urllist[j].split("/")[4]
        self.driver.get(self.urllist[j])

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

    def getPageData(self):
        self.data = ""
        self.images = []

        game_img = self.driver.find_element(
            By.CLASS_NAME, 'img-responsive').get_attribute("src")
        self.images.append(game_img)

        for i in range(1, 5):
            game_images = self.driver.find_element(
                by=By.XPATH, value=f'//div[@class="summary-media-grid-row"]/div[{i}]/a/img').get_attribute('src')
            self.images.append(game_images)
            sleep(2)

        game_rank = self.driver.find_element(
            by=By.CLASS_NAME, value='game-header-ranks').find_elements(by=By.TAG_NAME, value='a')
        # if there are 2 ranks - overall and strategy, if there are 3, add overall and thematic
        game_name = self.driver.find_element(
            by=By.XPATH, value=f'//div[2][@class="game-header-title-info"]/h1/a').text

        #
        min_players = self.driver.find_element(
            by=By.XPATH, value=f'//div[1][@class="gameplay-item-primary"]/span/span[1]').text

        #
        try:
            max_players = self.driver.find_element(
                by=By.XPATH, value=f'//div[1][@class="gameplay-item-primary"]/span/span[2]').text[1:]
        except:
            max_players = min_players
        #
        min_time = self.driver.find_element(
            by=By.XPATH, value=f'//ul[@class="gameplay"]/li[2]/div/span/span/span').text
        try:
            max_time = self.driver.find_element(
                by=By.XPATH, value=f'//div[1][@class="gameplay-item-primary"]/span/span/span[2]').text[1:]
        except:
            max_time = min_time
        designer = self.driver.find_element(
            by=By.XPATH, value=f'//div[@class="credits ng-scope"]/ul/li[1]/popup-list/span/a').text
        if len(game_rank) == 2:
            ranks = {"overall": game_rank[0].text,
                     "strategy": game_rank[1].text}
        if len(game_rank) == 3:
            ranks = {
                "overall": game_rank[0].text, "thematic": game_rank[1].text, "strategy": game_rank[2].text}

        self.data = {"uuid": str(uuid.uuid4()), "id": self.URL.split('/')[4], "url": self.URL, "name": game_name, "img": self.images[0],
                     "ranks": ranks,
                     "min_players": min_players, "max_players": max_players, "min_time": min_time,
                     "max_time": max_time,
                     "designer": designer}

    def writeData(self):
        if os.path.exists(self.target_dir) == False:
            os.mkdir(self.target_dir)
            sleep(2)
            os.chdir(self.target_dir)
            # replace x with w for if it doesn't exist
            file = open("data.json", "w")
            file.write(f'"{self.data}"')
            file.close()

    def saveImages(self):
        if os.path.exists('./images') == False:
            os.mkdir('./images')
            os.chdir('./images')

            for i in range(0, len(self.images)):
                urllib.request.urlretrieve(
                    self.images[i], f'{self.URL.split("/")[4]}_{i}.jpg')


def getInfo(urllist):
    info = PageScraper(urllist)
    for j in range(0, len(urllist)):
        info.goToPage(j)
        sleep(2)
        info.bypassCookies()
        sleep(2)
        info.getPageData()
        sleep(2)
        info.writeData()
        sleep(2)
        info.saveImages()
        sleep(2)


if __name__ == "__main__":
    urllist = links
    getInfo(urllist)
    sleep(2)
    print('exit')
