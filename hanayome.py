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
			print("[FAILED]: Error opening page!")
			exit()

	def getAllChapter(self,manga_path,pages):
		try:
			allChapter = []
			for i in range(pages):
				chapter_page = self.getPageChapter(manga_path,i+1)
				allChapter = allChapter + chapter_page
			return allChapter
		except:
			print("[FAILED]: Error getting all chapters")
			exit()

	def getPageChapter(self,manga_path,page):
		try:
			page_link = manga_path+"/chapters/"+str(page)
			self.driver.get(page_link)
			soup = BeautifulSoup(self.driver.page_source,'html.parser')
			info = soup.findAll("div", {"data-lang": "1"})

			list_chapter = []
			for i in range(len(info)):
				chapter = {}
				chapter['id'] = info[i]['data-id']
				chapter['chapter'] = info[i]['data-chapter']
				chapter['title'] = info[i]['data-title']
				list_chapter.append(chapter)
			
			return list_chapter
		except:
			print("[FAILED]: Error getting chapters in page")
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

	print("Getting All Chapters...")
	allChapters = myManga.getAllChapter(config['MANGA_PATH'],pages)
	print("[SUCCESS]: Found "+str(len(allChapters))+" Chapters")

	print("Closing Chrome...")
	myManga.closeDriver()
	print("[DONE]: Happy Reading.")


if __name__ == '__main__':
	main()
