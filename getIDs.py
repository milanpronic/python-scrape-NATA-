import requests
from bs4 import BeautifulSoup
import csv


input_file = csv.DictReader(open("IDS.csv"))
existIds = [row['id'] for row in input_file]

dict_writer = csv.DictWriter(open('IDS.csv', 'a+', newline=''), ["id", "link"])
if(len(existIds) == 0): dict_writer.writeheader()

for pageid in list(range(1,430)):
    print(pageid)
    url = 'https://www.nata.com.au/accredited-facility/?page=%d&sortby=Site_name&str=&&BEName= ' % (pageid)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.select('.animatebottom table')
    rows = table[0].find_all('tr')
    for i, row in enumerate(rows): 
        if(i % 2 == 0): continue
        aTag = row.find('a')
        if(aTag):
            id = aTag.string
            if(id in existIds):
                continue
            dict_writer.writerow({"id": id, "link": aTag['href']})
