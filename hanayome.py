import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import configparser

class MangaDex:
	options = None
	driver = None

	def __init__(self, driver_path):
		self.options = webdriver.ChromeOptions()
		# self.options.add_argument('--headless')
		self.options.add_argument('--incognito')
		# self.options.add_argument('window-size=1200x600')
		self.driver = webdriver.Chrome(driver_path,options=self.options)
	
	def openManga(self,manga_path):
		self.driver.get(manga_path)
		time.sleep(2)

	def closeDriver(self):
		self.driver.quit()



def configRead():
	configs = configparser.ConfigParser()
	configs.read('config.ini')
	config = {}
	config['USERNAME'] = configs['USER']['USERNAME']
	config['PASSWORD'] = configs['USER']['PASSWORD']
	config['DRIVER_PATH'] = configs['LOCATION']['DRIVER_PATH']
	config['MANGA_PATH'] = configs['LOCATION']['MANGA_PATH']

	return config

def main():
	config = configRead()

	myManga = MangaDex(config['DRIVER_PATH'])
	myManga.openManga(config['MANGA_PATH'])
	myManga.closeDriver()


if __name__ == '__main__':
	main()


# html = driver.find_elements_by_xpath("//div[@data-lang='1']")
# print(html[0].text)

