import connect
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
import boto3
# Let's start by telling to boto3 that we want to use an S3 bucket
import connect
import json


class PageScraper:

    def __init__(self, urllist):
        options = Options()
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        self.data = {}
        self.images = []
        self.cwd = os.getcwd()
        self.urllist = urllist
        self.URL = self.urllist[0]  # initial value
        self.saveToMemory = ''
        self.uploadToAWS = ''
        # initialise values to see if data is repeated, [memory, AWS]
        self.uploadRepeat = False
        self.awsRepeat = False
        self.URL = self.urllist[0]  # new page
        self.target_dir = self.cwd + \
            '/raw_data/' + urllist[0].split("/")[4]  # new folder

    def checkSaveLocation(self):
        print('save to memory, y/n')
        self.saveToMemory = input()
        while self.saveToMemory not in ['y', 'Y', 'n', 'N']:
            print('save to memory, type y or n')
            self.saveToMemory = input()

        print('upload to AWS, y/n')
        self.uploadToAWS = input()
        while self.uploadToAWS not in ['y', 'Y', 'n', 'N']:
            print('upload To AWS, type y or n')
            self.uploadToAWS = input()

    def check_repeat_data(self, j):
        if self.saveToMemory == 'y':
            # upload url from json
            self.uploadRepeat = False
        else:
            pass

        if self.uploadToAWS == 'y':
            # use SQL to check if url is in urllist
            self.awsRepeat = False
        else:
            pass

    def goToPage(self, j):
        self.URL = self.urllist[j]  # new page
        self.target_dir = self.cwd + \
            '/raw_data/' + urllist[j].split("/")[4]  # new folder
        self.driver.get(self.urllist[j])  # goes to site

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
        # check if data has already been added
        self.data = {}
        self.images = []
        try:
            game_img = self.driver.find_element(
                By.CLASS_NAME, 'img-responsive').get_attribute("src")
            self.images.append(game_img)
        except:
            pass

        for i in range(1, 5):
            try:
                game_images = self.driver.find_element(
                    by=By.XPATH, value=f'//div[@class="summary-media-grid-row"]/div[{i}]/a/img').get_attribute('src')
                self.images.append(game_images)
                sleep(2)
            except:
                pass

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
            max_players = int(self.driver.find_element(
                by=By.XPATH, value=f'//div[1][@class="gameplay-item-primary"]/span/span[2]').text[1:])

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
        try:
            designer = self.driver.find_element(
                by=By.XPATH, value=f'//div[@class="credits ng-scope"]/ul/li[1]/popup-list/span/a').text
        except:
            designer = self.driver.find_element(
                by=By.XPATH, value=f'//div[@class="credits ng-scope"]/ul/li[2]/popup-list/span/a').text
        if len(game_rank) == 2:
            rank_numbers = f"{game_rank[0].text}, {game_rank[1].text}"
        if len(game_rank) == 3:
            rank_numbers = f"{game_rank[0].text}, {game_rank[1].text}, {game_rank[2].text}"

        self.data = {"uuid": str(uuid.uuid4()), "id": self.URL.split('/')[4], "url": self.URL, "game_name": game_name, "img": self.images[0],
                     "rank_names": "overall, thematic, strategy", "rank_numbers": rank_numbers,
                     "min_players": min_players, "max_players": max_players, "min_time": min_time,
                     "max_time": max_time,
                     "designer": designer}

    def createDirectory(self):
        if os.path.exists(self.target_dir) == False:
            os.mkdir(self.target_dir)
            sleep(2)
        os.chdir(self.target_dir)

    def writeData(self):
        # replace x with w for if it doesn't exist
        file = open("data.json", "w")
        file.write(f'{json.dumps(self.data)}')
        file.close()

    def saveImages(self):
        if os.path.exists('./images') == False:
            os.mkdir('./images')
            os.chdir('./images')
            s3_client = boto3.client('s3')
            sleep(1)
            for i in range(0, len(self.images)):
                urllib.request.urlretrieve(
                    self.images[i], f'{self.URL.split("/")[4]}_{i}.jpg')
                response = s3_client.upload_file(
                    f'{self.URL.split("/")[4]}_{i}.jpg', 'bggdata', f'{self.URL.split("/")[4]}_{i}.jpg')

    def uploadData(self):
        # add try/effect or if statements to check types
        uuid = self.data['uuid']
        id = self.data['id']
        url = self.data['url']
        game_name = self.data['game_name']
        img = self.data['img']
        rank_names = self.data['rank_names']
        rank_numbers = self.data['rank_numbers']
        min_players = self.data['min_players']
        max_players = self.data['max_players']
        min_time = self.data['min_time']
        max_time = self.data['max_time']
        designer = self.data['designer']
        insert_cmd = f'''INSERT INTO games VALUES ('{uuid}', {id}, '{url}', '{game_name}', '{img}', '{rank_names}', '{rank_numbers}', {min_players}, {max_players}, {min_time}, {max_time}, '{designer}');'''
        connect.engine.execute(insert_cmd)


def getInfo(urllist):
    info = PageScraper(urllist)
    info.checkSaveLocation()

    for j in range(0, len(urllist)):
        info.check_repeat_data(j)  # check if data has been collected
        if (info.uploadRepeat == False and info.saveToMemory == 'y') or (info.awsRepeat == False and info.uploadToAWS == 'y'):  # set to only go to page if up
            info.goToPage(j)
            sleep(2)
            info.bypassCookies()
            info.getPageData()
            info.createDirectory()
            if info.saveToMemory == 'y':
                info.writeData()
            if info.uploadToAWS == 'y':
                info.saveImages()
                sleep(2)
                info.uploadData()

            sleep(2)


if __name__ == "__main__":
    urllist = links
    getInfo(urllist)
    sleep(2)
    print('exit')
