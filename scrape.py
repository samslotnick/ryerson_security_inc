from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
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
            location = paras[7].text
        else:    
            location = paras[8].text
        if paras[5].text != "DATE AND TIME OF INCIDENT":
            date = paras[5].text
        else:
            date = paras[6].text
        nature = soup2.find_all("h1")
        nature = nature[2].text.rstrip()
        stats.append({"nature": nature, "date": date, "location":location})
    page += 10
print("----- %s seconds ----" % (time.time() - start_time))




#==============================================================================
# descrip_info    attempted    weapon knife rock arrest made  
#==============================================================================
