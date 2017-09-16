from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import json
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
api_key = config['KEYS']['api_key']
#api_key='AIzaSyDMBNDabjlj7zqLLGjTyA-C7z0poNrHBLY'
def getGeo(location, api_key):
    streets = ["Alleyway","Alley","Sidewalk"]
    location_ar = location.replace(",","").split(" ")
    mod_location = ""
    for word in location_ar:
        if word.islower() != True and word.rstrip() not in streets or word.isdigit()== True:
            mod_location += word + " "
#    mod_location = location.lower()
    mod_location = mod_location.replace(","," ").replace("sidewalk","").replace("near","").replace("alleyway","")
    print(mod_location)
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    addL = "address=" + mod_location.replace(" ", "+") + "&key=" + api_key
    geoURL = base + addL
    response = urlopen(geoURL)
    jsonRaw = response.read()
    jsonData = json.loads(jsonRaw)
    if jsonData['status'] == 'OK':
        geoResult = jsonData['results'][0]['geometry']['location']
    else:
        geoResult = ""
    return geoResult  

page = 0
links = []
stats = []
import time
start_time = time.time()
while page < 50:
    rye_sec = "http://www.ryerson.ca/irm/alerts_reports/alerts/?center_uiwcolumns_conContainer_0_0_securityincidentlist_start=" + str(page) 
    ref_page = urlopen(rye_sec)
    soup = BeautifulSoup(ref_page, 'html.parser')
    page_i = soup.find_all('a')
    for line in page_i:
        line = line.get("href")
        if "Security_Incident_On_Campus" in line:
            links.append(line)
    for link in links:
        sec_url = "http://www.ryerson.ca/" + link[17:-5]
        sec_page = urlopen(sec_url)
        soup2 = BeautifulSoup(sec_page, 'html.parser')
        paras = soup2.find_all("p")
        if paras[7].text != "LOCATION OF INCIDENT":
            location = paras[7].text.rstrip()
        else:    
            location = paras[8].text.rstrip()
        if paras[5].text != "DATE AND TIME OF INCIDENT":
            date = paras[5].text.rstrip()
        else:
            date = paras[6].text.rstrip()
        nature = soup2.find_all("h1")
        nature = nature[2].text.rstrip()
#        getGeo(location, api_key)
        stats.append({"nature": nature, "date": date, "location":location, "geoLoc": getGeo(location, api_key)})
    page += 10
print("----- %s seconds ----" % (time.time() - start_time))
#print(stats)
#place = google_maps.search(location=paras[8].text)
#print(place)



#==============================================================================
# descrip_info    attempted    weapon knife rock arrest made  
#==============================================================================


