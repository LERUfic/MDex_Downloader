import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import configparser

class MangaDex:
	options = None
	driver = None

	def __init__(self, driver_path):
		try:
			self.options = webdriver.ChromeOptions()
			self.options.add_argument('--headless')
			self.options.add_argument('--incognito')
			self.options.add_argument('window-size=1200x600')
			self.driver = webdriver.Chrome(driver_path,options=self.options)
		except:
			print("[FAILED]: Cannot starting chrome!")
			exit()

	def openManga(self,manga_path):
		try:
			self.driver.get(manga_path)
			time.sleep(6)

			return self.driver.page_source
		except:
			print("[FAILED]: Cannot opening MDex!")
			exit()

	def getAllPage(self,manga_path):
		try:
			halaman=1
			while(1):
				page_link = manga_path+"/chapters/"+str(halaman)
				self.driver.get(page_link)
				if "No results found." in self.driver.page_source:
					return halaman-1
					break
				else:
					print("Page "+str(halaman)+" Found")
					halaman = halaman + 1
		except:
			print("[FAILED]:")
			exit()

	def closeDriver(self):
		try:
			self.driver.quit()
		except:
			print("[FAILED]: Cannot closing chrome!")
			exit()


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

	print("Trying to start chrome...")
	myManga = MangaDex(config['DRIVER_PATH'])
	print("[SUCCESS]: Opening chrome.")
	
	# print("Trying to open MDex...")
	# # page = myManga.openManga(config['MANGA_PATH'])
	# print("[SUCCESS]: Opening MDex.")

	print("Searching how many pagination...")
	pages = myManga.getAllPage(config['MANGA_PATH'])
	print("[FOUND]: "+str(pages)+" pages")



	print("Closing Chrome...")
	myManga.closeDriver()
	print("[DONE]: Happy Reading.")


if __name__ == '__main__':
	main()


# html = driver.find_elements_by_xpath("//div[@data-lang='1']")
# print(html[0].text)

