from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import getpass
import pandas as pd
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
import re
import time

nb_page = 101 #set up the number of pages to scrape

options = Options()
options.binary_location = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
driver_path = 'C:/Windows/chromedriver.exe'
driver = webdriver.Chrome(options = options, executable_path = driver_path)
driver.maximize_window()

url = 'https://www.doctolib.fr/dentiste/paris?page=' #set the url to scrape
driver.get(url)
time.sleep(5)

#accept the cookies
cookies = driver.find_element_by_xpath('//*[@id="didomi-notice-agree-button"]')
cookies.click()

#setup the database
d = pd.DataFrame({'name':[], 'number':[], 'price':[], 'address':[], 'zip_code':[], 'vital_card':[]})

#start scraping loop for the defined number of pages
for pages in range(1, nb_page):

	#links of all doctors of a single page
	doctorlink = driver.find_elements_by_xpath('//*[@class="dl-search-result"]/div[1]/div[1]/div[2]/h3/a')

	#create a loop that click on doctors link
	for doctorclick in doctorlink:

		#open doctor link in a new tab
		doctorclick.send_keys(Keys.CONTROL + Keys.RETURN)
		driver.switch_to_window(driver.window_handles[1])
		time.sleep(5)

		#scrape data
		try:
			name = driver.find_element_by_xpath('/html/body/div[6]/header/div/div/div[2]/h1').text
		except:
			name = ''

		try:
			rownumber = driver.find_element_by_xpath('/html/body/div[6]/div/div[1]/div[10]/div/div[2]/div/div[2]/div').text
		except:
			rownumber = ''
		number = re.sub(r'[A-Za-z]*[ X]*€*¬*é*:*\n*\?*\'*-*à*', '', rownumber) #clean the data to only get a the number in number

		try:
			rowprice = driver.find_element_by_xpath('/html/body/div[6]/div/div[1]/div[12]/div/div[2]/div[1]/div[2]').text
		except:
			rowprice = ''
		rowprice2 = re.sub(r'[A-Za-z]*[ X]*€*¬*é*:*\n*\?*\'*-*', '', rowprice) #clean the data to only get a the price in number
		price = re.sub(r'à[0-9]*$', '', rowprice2)

		try:
			address = driver.find_element_by_xpath('/html/body/div[6]/div/div[1]/div[6]/div/div[2]/div[1]/div').text
		except:
			address = ''

		try:
			zip_code = re.findall(r'75[0-9][0-9][0-9]', adress) #find the zip code in the address string
		except:
			zip_code = ''

		try:
			vital_card = driver.find_elements_by_xpath("//*[text()='Carte Vitale acceptée']") 
		except:
			vital_card = ''
		if vital_card is not None:
			vital_card = 'Carte Vitale acceptée'
		else:
			pass

		#append scraped data to the panda database
		doctor = {'name':name, 'number':number, 'price':price, 'address':address, 'zip_code':zip_code, 'vital_card':vital_card}

		d = d.append(doctor, ignore_index = True)
		print(d)
		driver.close()
		driver.switch_to_window(driver.window_handles[0])
		time.sleep(1)

	#click on next page button
	nextpage = driver.find_element_by_xpath('/html/body/div[7]/div/div[1]/div[11]/div[2]/a')
	nextpage.click()

#export to csv with ";""seperator because in France, separate with coma put every data in one column
d.to_csv('data_seleniuem.csv', sep=';', encoding='UTF-16LE')

driver.quit()
