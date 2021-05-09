import scrapy
import pandas as pd
import csv

#set the items output
class Doctor(scrapy.Item):
    name = scrapy.Field()
    number = scrapy.Field()
    price = scrapy.Field()
    address = scrapy.Field()
    vital_card = scrapy.Field()

class LinksSpider(scrapy.Spider):
    name = 'spider2'

    #open the "links.csv" previously created with spider1
    try:
        with open("links.csv", "rt") as f:
           start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    def parse(self, response):
        d = Doctor()

        try:
        	d['name'] = response.css('h1.dl-profile-header-name span::text').getall()
        except:
        	d['name'] = ''

        try:
        	d['number'] = response.css('div.dl-profile-box div.dl-display-flex::text').getall()
        except:
        	d['number'] = ''

        try:
        	d['price'] = response.css('.dl-profile-fee-tag::text').getall()
        except:
        	d['price'] = ''

        try:
        	d['address'] = response.css('h3.dl-profile-card-title+ .dl-profile-text > div::text').getall()
        except:
        	d['address'] = ''

        try:
        	d['vital_card'] = response.xpath('//div[text()="Carte Vitale acceptée"]/text()').getall()
        except:
        	d['vital_card'] = ''

        yield d
