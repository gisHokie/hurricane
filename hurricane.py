import requests, re, zipfile, io

def main():
    url_path = 'https://www.nhc.noaa.gov/gis/archive_forecast_results.php?id=all4&year=2018'
    base_url = 'https://www.nhc.noaa.gov/gis/'
        
    # get list of links to zip files
    zip_list = get_zip_list(url_path)
    
    strip_list = ['a href=', '\"']
    cleaned_links = []
    
    # clean zip list
    for i in zip_list:
        tmp = clean_zip_link(i, strip_list)
        cleaned_links.append(tmp)
           
    # request data from zip urls
    for i in cleaned_links:
        url = base_url + i
        r = get_http_request(url)
    
    # print files: .shp, .shx, .dbf; not .xml
    with zipfile.ZipFile(io.BytesIO(r.content)) as myfile:
        files = myfile.namelist()
        for i in files:
            if (re.match(r'.*\.shp', i) or re.match(r'.*\.shx', i) or re.match(r'.*\.dbf', i)) and not re.match(r'.*\.xml', i):
                print(i)
                print(myfile.read(i))
  
# parses list of links to zip files in html page  
def get_zip_list(url):
    # request url
    r = get_http_request(url)
    
    # get html
    html = r.text
    
    # find zips
    matches = re.findall(r'a href\=".*\.zip"', html)
    zip_list = []
    
    return zip_list

# strips unwanted strings from link
def clean_zip_link(zip, strip_list):
    for i in strip_list:
        zip = zip.strip(i)
    return zip

# todo
def write_files(zip):
    
    return 0
   
# makes http get request to url
def get_http_request(url):
    r = requests.get(url)
    if r.status_code != 200:
        sys.exit("the http request returned status code " + str(r.status_code))
    return r
    
if __name__== "__main__":
  main()
