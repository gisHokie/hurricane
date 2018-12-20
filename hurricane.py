import requests, re, zipfile, io

def main():
    url_path = 'https://www.nhc.noaa.gov/gis/archive_forecast_results.php?id=all4&year=2018'
    base_url = 'https://www.nhc.noaa.gov/gis/'
    
    zip_list = get_zip_list(url_path)
            
    for i in zip_list:
        url = base_url + i
        r = get_zip(url)
        
        filename = str(tmp) + '.zip'
        
        with zipfile.ZipFile(io.BytesIO(r.content)) as myfile:
            files = myfile.namelist()
            for i in files:
                if (re.match(r'.*\.shp', i) or re.match(r'.*\.shx', i) or re.match(r'.*\.dbf', i)) and not re.match(r'.*\.xml', i):
                    print(i)
                    myfile.extract(i)
                
def get_zip_list(url):
    # request url
    r = requests.get(url)
    if r.status_code != 200:
        raise
    
    # get html
    html = r.text
    
    # find zips
    matches = re.findall(r'a href\=".*\.zip"', html)
    zip_list = []

    # format zips
    for i in matches:
        i = i.strip('a href=')
        i = i.strip('\"')
        zip_list.append(i)
        
    return zip_list

def get_zip(url):
    r = requests.get(url)
    if r.status_code != 200:
        print(base_url + i)
        print(r.status_code)
        raise
    
    return r

def write_files(zip):
    
    return 0
    
    
    
if __name__== "__main__":
  main()
