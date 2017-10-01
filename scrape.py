from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import json
from geojson import Feature, Point, FeatureCollection
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
api_key = config['KEYS']['api_key']
def getGeo(location, api_key):
    streets = ["Alleyway","Alley","Sidewalk"]
    location_ar = location.replace(",","").split(" ")
    mod_location = ""
    for word in location_ar:
        if word.islower() != True and word.rstrip() not in streets or word.isdigit()== True:
            mod_location += word + " "
#    mod_location = location.lower()
    mod_location = mod_location.replace(","," ").replace("sidewalk","").replace("near","").replace("alleyway","")
#    print(mod_location)
    base = "https://maps.googleapis.com/maps/api/geocode/json?"
    addL = "address=" + mod_location.replace(" ", "+") + "&key=" + api_key
    geoURL = base + addL
    response = urlopen(geoURL)
    jsonRaw = response.read()
    jsonData = json.loads(jsonRaw)
    if jsonData['status'] == 'OK':
        geoResult = []
        geoResult.append(jsonData['results'][0]['geometry']['location']['lng'])
        geoResult.append(jsonData['results'][0]['geometry']['location']['lat'])
    else:
        geoResult = []
    return geoResult  

def arrestFormat(nature):
    if "Arrest Made in" in nature:
        nature = nature.partition("in ")[-1]
    else:
        nature = nature.partition(" -")[0]
    return nature

page = 0
links = []
collection = {"type":"FeatureCollection","features":[]}
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
        if "with a weapon" in nature.lower():
            weapon = nature.partition("(")[-1].replace(")","")
            nature = nature.partition("(")[0].rstrip()
        else: 
            weapon = False
        if "arrest made" in nature.lower():
            arrest = True
            nature = arrestFormat(nature)
        else:
            arrest = False
#        getGeo(location, api_key)
        if "arrest made" in nature.lower():
            print(nature)
        stats = {"type":"Feature","properties":{"nature": nature,"date": date,"location":location,"weapon": weapon,"arrest": arrest},"geometry":{"type": "Point","coordinates":getGeo(location, api_key)}}
        if len(stats["geometry"]["coordinates"]) > 0:
            final = json.dumps(stats)
#        print(stats)
        outfile = open("data.json","a",encoding='utf-8')
        outfile.write("\n"+final+",")
    page += 10
print("----- %s seconds ----" % (time.time() - start_time))
outfile.close()
#print(stats)
#place = google_maps.search(location=paras[8].text)
#print(place)



