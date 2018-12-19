###################################
#author: Scott D. McDermott
#date: 12/15/2018
#summary: Collect commpressed shapefiles from URL
###################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException  
from selenium.common.exceptions import NoSuchElementException

import requests, zipfile, io, os
import urllib
import json
import datetime

#Custom modules
import modules.file_scaper as fs
import modules.shapefile_to_postgres as stp

# Get the start date time to calculate time run
getDate = datetime.datetime.now()
print(getDate)

RETRIES = 3
TIMEOUT_SECONDS = 10
zip_dir = 'E:/platform/scripts/data/hurricanes'
getYear = '2018'
url_path = 'https://www.nhc.noaa.gov/gis/archive_forecast.php?year=' + getYear
hur_nhc_XPATH_pre = '/html/body/div[5]/div/table/tbody/tr['
hur_nhc_XPATH_post = ']/td[1]'
hur_name_XPATH_pre = '/html/body/div[5]/div/table/tbody/tr['
hur_name_XPATH_post = ']/td[2]/a'
geckoDriverPath = r"D:\drivers\geckodriver.exe"
binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'

# Create the Year Directory if not exist
zip_path_year = zip_dir +  '/' + getYear
if not os.path.exists(zip_path_year):
    os.makedirs(zip_path_year)

# get the firefox driver
driver = fs.get_firefox_driver_url(url_path, binary_path)
	
# Loop through the HTML and read if only end point is *.SHP
# Use XPATH to locate the HREF and file name path
i = 2
hur_nhc_XPATH = hur_nhc_XPATH_pre + str(i) + hur_nhc_XPATH_post
hur_name_XPATH = hur_name_XPATH_pre + str(i) + hur_name_XPATH_post
elem_nhc = driver.find_element_by_xpath(hur_nhc_XPATH)
elem_name = driver.find_element_by_xpath(hur_name_XPATH)
nhc_list = []

if(elem_nhc):
	while (elem_nhc is not None and elem_name is not None ):
		hur_nhc_XPATH = '/html/body/div[5]/div/table/tbody/tr[' + str(i) + ']/td[1]'
		hur_name_XPATH = '/html/body/div[5]/div/table/tbody/tr[' + str(i) + ']/td[2]/a'
		i += 1
		try:
			# Get the Element 
			elem_nhc = driver.find_element_by_xpath(hur_nhc_XPATH)
			elem_name = driver.find_element_by_xpath(hur_name_XPATH)
			text_nhc = elem_nhc.text
			text_name = elem_name.text
			full_text = text_nhc + ',' + text_name
			print(full_text)
			nhc_list.append(full_text)
		# https://stackoverflow.com/questions/9221583/set-up-a-default-exception-handler-when-unable-to-locate-an-element-in-selenium
		except (NoSuchElementException):
			# raise ("Element with id=%s was not found." % id)
			 break

print(nhc_list)
#dump to JSON
full_path = zip_path_year + '/code' + getYear + '.json' 
with open(full_path, 'w') as outfile:
    json.dump(nhc_list, outfile)


#Close the driver
driver.close();

getDate2 = datetime.datetime.now()
print(getDate2)
