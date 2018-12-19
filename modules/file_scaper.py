###################################
#author: Scott D. McDermott
#date: 12/15/2018
#summary:
###################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException  
from selenium.common.exceptions import NoSuchElementException

import requests, zipfile, io, os
import urllib
from pathlib import Path
import json

class Scraper:

	def __init__(self):
		self.data = []
		
	def file_exist(self, file_path):
		bool_file = True
		get_file = Path(file_path)
		bool_file =  get_file.is_file()
		return bool_file
		
	# Create a year directory if it does not exist
	def create_dir_by_year(self, zip_path_year):
		if not os.path.exists(zip_path_year):
			os.makedirs(zip_path_year)
		
	# Create a Selenium Firefox driver to scrape the data from browser
	# Need to download the geckoDriverPath and save to known directory
	def get_firefox_driver_url(self, url_path, binary_path):
		binary = FirefoxBinary(binary_path)
		driver = webdriver.Firefox(firefox_binary=binary)
		driver.get(url_path)
		return driver

	# Loop through the HTML and read if only end point is *.SHP
	# Use XPATH to locate the HREF and file name path
	def get_text_by_attribute(self, t, attrib):
		getHrefValue = t.get_attribute(attrib)
		getTxtValue = t.text
		full_Href_Txt_Value = getHrefValue + ',' + getTxtValue
		return (full_Href_Txt_Value)

	# https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
	def get_list_files_from_directory(self, dirName):
		# create a list of file and sub directories 
		# names in the given directory 
		listOfFile = os.listdir(dirName)
		allFiles = list()
		# Iterate over all the entries
		for entry in listOfFile:
			# Create full path
			fullPath = os.path.join(dirName, entry)
			# If entry is a directory then get the list of files in this directory 
			if os.path.isdir(fullPath):
				allFiles = allFiles + self.get_list_files_from_directory(fullPath)
			else:
				allFiles.append(fullPath)
					
		return (allFiles) 
		
	# Download zip file and save with hurricane name
	# Uncompress the Zip files and store in separate directory
	def extract_zipname(self, zip_path,zip_file_url):
		print('Extracting: ' + zip_file_url)
		r = requests.get(zip_file_url)
		z = zipfile.ZipFile(io.BytesIO(r.content))
		z.extractall(zip_path)	

#if __name__ == '__main__':

