import requests
import csv
from bs4 import BeautifulSoup
from bs4 import Tag
import re

input_file = csv.DictReader(open("data.csv"))
existIds = [row['ID'] for row in input_file]

dict_writer = csv.DictWriter(open('data.csv', 'a+', newline=''), ["ID", "Company_Name", 'Address', 'Phone', 'Email', 'Website', 'Contact_Name'])
if(len(existIds) == 0): dict_writer.writeheader()


input_file = csv.DictReader(open("IDS.csv"))
for row in input_file:
    if(row['id'] in existIds): continue
    print(row['id'])
    url = 'https://www.nata.com.au' + row['link']
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.select('.page-title strong')[0]
    info = {'ID': row['id'], 'Company_Name': '', 'Address': '', 'Phone': '', 'Email': '', 'Website': '', 'Contact_Name': ''}
    if(title.string):
        info['Company_Name'] = title.string
    else:
        info['Company_Name'] = ' '.join(string for string in title.stripped_strings)
    address_strong = soup.find('strong', string=re.compile("Address Details:"))
    address_strong = address_strong.next_sibling
    while address_strong:
        if(isinstance(address_strong, Tag)): 
            if(address_strong.name == 'a'): break
            address_strong = address_strong.next_sibling
            continue
        if(info['Address'] != ''): info['Address'] += ' '
        info['Address'] += address_strong.strip()
        address_strong = address_strong.next_sibling
    if(address_strong): address_strong = address_strong.next_sibling.next_sibling
    if(address_strong): info["Website"] = address_strong['href']
    address_strong = soup.find('strong', string=re.compile("Contact Details:"))
    for i, br in enumerate(address_strong.parent.find_all('br')):
        if(i == 1): 
            if(br.next_sibling): info['Contact_Name'] = br.next_sibling.strip()
        if(i == 2): 
            if(br.next_sibling): info['Phone'] = br.next_sibling.strip()
        if(i == 3): 
            if(br.next_sibling): info['Email'] = br.next_sibling['src'][26:]
    print(info)
    exit()
    dict_writer.writerow(info)