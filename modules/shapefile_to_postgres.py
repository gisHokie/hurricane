###################################
#author: 
#date:
#summary:
# Go to directory where shp is located
# Read each sub folders
# Locate SHP, DBF, and SHX
# Get the Path and file name of the SHP
# Add SHP file name to CMD and Execute
# http://www.bostongis.com/pgsql2shp_shp2pgsql_quickguide.bqg
# 
###################################

import os
import subprocess
from os import listdir
from os.path import isfile, join


#https://gis.stackexchange.com/questions/258052/how-to-specify-a-password-with-shp2pgsql-using-centos
def shp_to_postgres(cmd):
	# Execute command to post shapes to postgres
	subprocess.call(cmd, shell=True)