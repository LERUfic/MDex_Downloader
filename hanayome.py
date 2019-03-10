import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import configparser

class MangaDex:
	options = None
	driver = None
	manga_path = None

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

	def setMangaPath(self,manga_path):
		self.manga_path = manga_path

	def openManga(self):
		try:
			self.driver.get(self.manga_path)
			time.sleep(6)

			return self.driver.page_source
		except:
			print("[FAILED]: Cannot opening MDex!")
			exit()

	def getAllPage(self):
		try:
			halaman=1
			while(1):
				page_link = self.manga_path+"/chapters/"+str(halaman)
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

	def getAllChapters(self,pages):
		try:
			allChapters = []
			for i in range(pages):
				chapter_page = self.getPageChapter(i+1)
				allChapters = allChapters + chapter_page
			return allChapters
		except:
			print("[FAILED]: Error getting all chapters!")
			exit()

	def createMainFolder(self, allChapters):
		try:
			# folder = re.findall(r"\w+[0-9]",self.manga_path)
			folder = self.manga_path.split("/")
			main_folder = folder[-2]+"-"+folder[-1]
			access_rights = 0o755
			if(os.path.isdir(main_folder)):
				print("Main Folder %s exist" % main_folder)
			else:
				try:
					os.mkdir(main_folder, access_rights)
				except OSError:
					print ("[FAILED] Cannot create %s " % main_folder)
				else:
					print ("[SUCCESS] Created %s" % main_folder)

			for i in range(len(allChapters)):
				self.downloadImage(main_folder,allChapters[i])

		except:
			print("[FAILED]: Cannot create main folder!")
			exit()

	def downloadImage(self,base_folder,chapter):
		try:
			named_folder = chapter["chapter"]+" - "+chapter["title"]+" - "+chapter["id"]
			chapter_folder = base_folder+"/"+named_folder
			if(os.path.isdir(chapter_folder)):
				print("Chapter Folder %s exist" % chapter_folder)
			else:
				try:
					access_rights = 0o755
					os.mkdir(chapter_folder, access_rights)
				except OSError:
					print ("[FAILED] Cannot create %s " % chapter_folder)
				else:
					print ("[SUCCESS] Created %s" % chapter_folder)
		except:
			print("[FAILED]: Cannot create chapter folder!")
			exit()

	def getPageChapter(self,page):
		try:
			page_link = self.manga_path+"/chapters/"+str(page)
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
	try:
		configs = configparser.ConfigParser()
		configs.read('config.ini')
		config = {}
		config['USERNAME'] = configs['USER']['USERNAME']
		config['PASSWORD'] = configs['USER']['PASSWORD']
		config['DRIVER_PATH'] = configs['LOCATION']['DRIVER_PATH']
		config['MANGA_PATH'] = configs['LOCATION']['MANGA_PATH']

		return config
	except:
		print("[FAILED]: Cannot read config.ini")
		exit()

def main():
	config = configRead()

	print("Trying to start chrome...")
	myManga = MangaDex(config['DRIVER_PATH'])
	print("[SUCCESS]: Opening chrome.")
	
	print("Trying to set Manga Url...")
	myManga.setMangaPath(config['MANGA_PATH'])
	print("[SUCCESS]: Set Manga Url.")

	print("Searching how many pagination...")
	pages = myManga.getAllPage()
	print("[FOUND]: "+str(pages)+" pages")

	print("Getting All Chapters...")
	allChapters = myManga.getAllChapters(pages)
	print("[SUCCESS]: Found "+str(len(allChapters))+" Chapters")

	myManga.createMainFolder(allChapters)

	print("Closing Chrome...")
	myManga.closeDriver()
	print("[DONE]: Happy Reading.")


if __name__ == '__main__':
	main()
