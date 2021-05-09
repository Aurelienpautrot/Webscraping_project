from urllib import request
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as BS
import re
import pandas as pd

nb_page = 101  #set up the number of pages to scrape
url = 'https://www.doctolib.fr/dentiste/paris?page='   #setup url

#create the list of links directing to doctors info
doctorlinks = []

#create a loop to scrape the links for the defined number og pages
for page in range(1, nb_page):
	
	UserAgent = Request(url + str(page), headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'})
	html = request.urlopen(UserAgent)
	bs = BS(html.read(), 'html.parser')
	
	#Create the real links and add them to the database
	tags = bs.find_all('a', {'class':'dl-search-result-name js-search-result-path'})

	for tag in tags:
		links = ['https://www.doctolib.fr/' + tag['href']]
		doctorlinks.extend(links)
	print(doctorlinks)

#setup the database
d = pd.DataFrame({'name':[], 'number':[], 'price':[], 'address':[], 'zip_code':[], 'vital_card':[]})

#create a loop to scrape doctors pages
for doctorsinfo in doctorlinks:
	print(doctorsinfo)

	UserAgent = Request(doctorsinfo, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'})
	html = request.urlopen(UserAgent)
	bs = BS(html.read(), 'html.parser')

#scrape data
	try:
		name = bs.find('h1').text
	except:
		name = ''

	try:
		rownumber = bs.find('div', {'class':'dl-display-flex'}).text
	except:
		rownumber = ''
	number = re.sub(r'[A-Za-z]*[ X]*€*¬*é*:*\n*\?*\'*-*à*', '', rownumber) #clean the data to only get the number in number

	try:
		rowprice = bs.find('div', {'class':'dl-profile-fee-tag'}).text
	except:
		rowprice = ''
	rowprice2 = re.sub(r'[A-Za-z]*[ X]*€*¬*é*:*\n*\?*\'*-*', '', rowprice) #clean the data to only get a the price in number
	price = re.sub(r'à[0-9]*$', '', rowprice2)

	try:
		address = bs.find('div', {'class':'dl-profile-practice-name'}).parent.text
	except:
		address = ''

	try:
		zip_code = re.findall(r'75[0-9][0-9][0-9]', adress) #find the zip code in the address string
	except:
		zip_code = ''

	try:
		vital_card = bs.find('div',string = 'Carte Vitale acceptée').text
	except:
		vital_card = ''


#output the data
	doctor = {'name':name, 'number':number, 'price':price, 'address':address, 'zip_code':zip_code, 'vital_card':vital_card}

	d = d.append(doctor, ignore_index = True)
	print(d)

#export to csv
d.to_csv('data_bs.csv', sep=';', encoding='UTF-16LE')
