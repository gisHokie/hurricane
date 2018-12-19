###################################
#author: Scott D. McDermott
#date: 12/15/2018
#summary: Collect commpressed shapefiles from URL
# test urls
#'https://download.bbbike.org/osm/bbbike/Albuquerque/'
# 'https://download.bbbike.org/osm/bbbike/Albuquerque/'
# 'http://osm2shp.ru/'
###################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException  
from selenium.common.exceptions import NoSuchElementException

import requests, zipfile, io, os, sys
import urllib
import json
import datetime

#Custom modules
import modules.file_scaper as fs
import modules.shapefile_to_postgres as stp

RETRIES = 3
TIMEOUT_SECONDS = 10
zip_dir = 'E:/platform/scripts/data/hurricanes'
#getYear = '2018'
get_hur_id = 'al14'
# get specifice hurricane for test purposes
# url_path = 'https://www.nhc.noaa.gov/gis/archive_forecast_results.php?id=' + get_hur_id + '&year=' + getYear
# # Get all hurricanes for a given year
# #url_path = 'https://www.nhc.noaa.gov/gis/archive_forecast_results.php?'&year=' + getYear
file_ext = 'zip'
pre_XPATH = '//a[contains(@href,\''
post_XPATH = '\')]'
geckoDriverPath = r"D:\drivers\geckodriver.exe"
binary_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
port = 4326
# shp_dir = r'E:/platform/scripts/data/hurricanes/' + str(getYear)
shp_ext = 'shp'
hostname = 'localhost'
dbasename = 'geo'
username = 'postgres'
pwd = 'admin'
get_attrib = 'href'

# Instantiate the scaper class
spr = fs.Scraper()

# Get the start date time to calculate time run
getDate = datetime.datetime.now()
print(getDate)

now = datetime.datetime.now()
getYear = now.year
getDecade = getYear - 10
full_XPATH = pre_XPATH + file_ext + post_XPATH
shp_list = []

# WHILE LOOP for a given year (??Need to check if hurricane exist?)
# Do we need a loop as ideally we will be getting the most current data after collecting all archives??
#while(getYear >= getDecade):
shp_dir = r'E:/platform/scripts/data/hurricanes/' + str(getYear)
url_path = 'https://www.nhc.noaa.gov/gis/archive_forecast_results.php?id=' + get_hur_id + '&year=' + str(getYear)
# Get all hurricanes for a given year
#url_path = 'https://www.nhc.noaa.gov/gis/archive_forecast_results.php?'&year=' + getYear
file_ext = 'zip'

# Create the Year Directory if not exist
zip_path_year = zip_dir +  '/' + str(getYear)
spr.create_dir_by_year(zip_path_year)

# Update getYear for next loop
getYear -= 1

# Verify Firefox Driver exist.
# If no drier found stop the script
firefox_exist = spr.file_exist(binary_path)
if (firefox_exist == False):
	sys.exit("No Firefox executable found")

# get the firefox driver
driver = spr.get_firefox_driver_url(url_path, binary_path)
	
# https://stackoverflow.com/questions/14974508/how-to-find-if-a-text-exists-on-page
textName = driver.find_elements_by_xpath(full_XPATH)

# get the shapefile names in a list
shp_list = []
for t in textName:
	get_shp_attrib = spr.get_text_by_attribute(t, get_attrib)
	shp_list.append(get_shp_attrib)
#Close the driver
driver.close();

# extract the files from the compressed folders
for z_url in shp_list:
	split_z = z_url.split(',')
	zip_file_url = split_z[0]
	zip_name = split_z[1]
	# split the file name to get only name and not name.shp extension
	splitname = zip_name.split('.')
	shp_name = splitname[0]
	zip_path = zip_path_year + '/' + shp_name

	spr.extract_zipname(zip_path,zip_file_url)


file_list = []
shp_list2 = []
# Create a list all files in the directories and sub directories
file_list = spr.get_list_files_from_directory(shp_dir)
# Create list of all shapefiles in the decompressed folders
for fl in file_list:
	split_onlyfiles = fl.split('.')
	len_split = len(split_onlyfiles)
	if (split_onlyfiles[len_split -1].upper() == 'shp'.upper()):
		shp_list2.append(fl)

		
# # UNCOMMENT THIS WHEN READY TO POST TO POSTGRESPost the shapes to Postgres
# for shp_path in shp_list2:
	# cmd = 'shp2pgsql -s ' + str(port) + ' ' + shp_path + ' | psql -h ' + hostname +  ' -d ' + dbasename + ' -U ' + username + ' PGPASSWORD ' + pwd + ' -q'
	# stp.shp_to_postgres(cmd)



getDate2 = datetime.datetime.now()
print(getDate2)