from collections import defaultdict
from configparser import ConfigParser
from urllib.parse import urlparse
import urllib

import psycopg2
import scrapy

# -*- coding: utf-8 -*

import scrapy
import re
import unicodedata
from scrapy.crawler import CrawlerProcess

from configparser import ConfigParser
from configdb import configdb

class InfoboxSpider(scrapy.Spider):
    name = 'simple'



    from configparser import ConfigParser
    def start_requests(self):
        urls = ['http://www.google.com/search?q=California+State+University+Fresno']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        def _clean(value):
            value = ' '.join(value)
            value = value.replace('\n', '')
            value = unicodedata.normalize("NFKD", value)
            value = re.sub(r' , ', ', ', value)
            value = re.sub(r' \( ', ' (', value)
            value = re.sub(r' \) ', ') ', value)
            value = re.sub(r' \)', ') ', value)
            value = re.sub(r'\[\d.*\]', ' ', value)
            value = re.sub(r' +', ' ', value)
            value = value.replace('"', '')
            return value.strip()



        strings = []

        try:
            # response.selector.xpath('//span/text()').get()

            address1 = response.xpath('//*').extract_first()
            print("address1? ")
            print(str(address1))
            if(len(address1)>0):
                text = _clean(address1[0].extract())
               # print("getting address: {}".format(text))
                strings.append(text)
        except Exception as error:
            strings.append(str(error))
        # print("printing strings")
        # print(strings)