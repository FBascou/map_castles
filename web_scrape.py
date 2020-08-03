import requests
from bs4 import BeautifulSoup
from time import sleep
from lxml import etree
import re
import json
import random

base_url = 'http://www.topcastles.com/'
castle_url = 'kastelen.php?SubMenu=main&SelCastle=krak&Language=en'
coor_regex = re.compile(r'-?\d{1,3}\.\d+')
castles = []
user_agent_list = [
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
]

def get_castle_info(soup):
	castle_info = soup.find_all('div', {'class':'feature'})
	return castle_info

def update_url():
	next_btn = soup.find('div', id='sectionLinks')('li')[0]
	return next_btn.find('a')['href'] if next_btn else None

def create_castle(castle_html):
	for item in castle_html:
		castle_dict = {}
		try:
			castle_dict['Name'] = item.find('h2', {'id':'top'}).text
		except: 
			castle_dict['Name'] = None
		try:
			castle_dict['Country'] = item.find_all('td')[14].text.replace("\n", "").replace("\t", "")
		except: 	
			castle_dict['Country'] = None
		try:
			castle_dict['Place'] = item.find_all('td')[22].text.replace("\n", "").replace("\t", "")
		except: 
			castle_dict['Place'] = None	
		try:
			castle_dict['Era'] = item.find_all('td')[26].text.replace("\n", "").replace("\t", "")
		except:
			castle_dict['Era'] = None
		try:
			castle_dict['Type'] = item.find_all('td')[24].text.replace("\n", "").replace("\t", "").replace("\n", "").replace("\t", "")
		except:
			castle_dict['Type'] = None
		try:
			castle_dict['Condition'] = item.find_all('td')[28].text.replace("\n", "").replace("\t", "")
		except:
			castle_dict['Condition'] = None
		try:	
			castle_dict['Description'] = item.find_all('td')[32].text.replace("\n", "").replace("\t", "")
		except:
			castle_dict['Description'] = None
		try:
			castle_dict['Latitude'] = coor_regex.findall(item.find_all('td')[38].text)[0].replace("\n", "").replace("\t", "")
		except:
			castle_dict['Latitude'] = None
		try:
			castle_dict['Longitude'] = coor_regex.findall(item.find_all('td')[38].text)[1].replace("\n", "").replace("\t", "")
		except:
			castle_dict['Longitude'] = None

		return castle_dict

while castle_url:
	user_agent = random.choice(user_agent_list)
	headers = {'User-Agent': user_agent}

	res = requests.get(f"{base_url}{castle_url}", headers=headers, timeout=20)
	print(f"{base_url}{castle_url}")
	print(headers)
	soup = BeautifulSoup(res.content, "lxml-xml")

	current_castle_html = get_castle_info(soup)
	castle = create_castle(current_castle_html)
	castles.append(castle)

	castle_url = update_url()
	if castle_url == '':
		break

	with open("castle_archive.json", "w") as outfile:
		json.dump(castles, outfile)

	sleep(10)