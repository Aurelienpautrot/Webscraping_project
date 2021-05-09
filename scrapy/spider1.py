import scrapy
from scrapy import Selector
from urllib import request
import pandas as pd

#choose the number of pages to scrape
nb_page = 101

#define the item link
class Link(scrapy.Item):
    link = scrapy.Field()

class LinkListsSpider(scrapy.Spider):
    name = 'spider1'
    page_number = 2
    start_urls = ['https://www.doctolib.fr/dentiste/paris?page=1']
    output = "output.csv"

    def parse(self, response): 

        #Gather the links of doctor pages      
        page_links_list = response.css('h3 a::attr(href)')

        for doctor_link in page_links_list:
        	l = Link()
        	l['link'] = 'https://www.doctolib.fr' + doctor_link.get()
        	yield l

        #go to the next page if the defined number of pages to scrape is not reach yet
        next_page = 'https://www.doctolib.fr/dentiste/paris?page='+ str(LinkListsSpider.page_number)
        if LinkListsSpider.page_number < nb_page:
        	LinkListsSpider.page_number = LinkListsSpider.page_number + 1
        	yield scrapy.Request(next_page, callback=self.parse)
