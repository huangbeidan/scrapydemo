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

id_dict = {}


class InfoboxSpider(scrapy.Spider):
    name = 'patent_spider_2'

    from configparser import ConfigParser
    # id_list = []
    # id_dict = defaultdict()

    def convert(self, item, value):
        listField = ["Industry", "Key people", "Subsidiaries"]
        if item in listField:
            print("item is the list: " + item)
            li = list(value.split(","))
            print("li is: " + str(li))
            return str(li)
        return value

    def connect(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        name_list = []
        global id_list

        try:
            # read connection parameters
            params = configdb()
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            # create a cursor
            cur = conn.cursor()
            # execute a statement
            cur.execute(
                'select distinct paperid, affiliation_colab from bd_patent where mark is null and mark2 is null;')
            # display the PostgreSQL database server version
            db_version = cur.fetchall()
            name_list = [tuple[1] for tuple in db_version]
            id_list = [tuple[0] for tuple in db_version]
            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
                return id_list, name_list

    # start_urls = ['https://en.wikipedia.org/wiki/Instagram']

    # Two ways of getting URLS

    def get_urls_fromDB(self, lines):
        querylist = []
        global id_list
        for i in range(len(lines)):
            if i < 20:
                cleaned = re.sub('[^0-9a-zA-Z ]+', ' ', lines[i])
                cleaned = re.sub('[ ]+', ' ', cleaned)
                cleaned = cleaned.strip().replace(" ", "_")
                cleaned = re.sub(r"\(.*\)", "", cleaned)
                querylist.append(cleaned)
                id_dict[cleaned] = id_list[i]
        output_url = ["https://en.wikipedia.org/wiki/" + x for x in querylist]
        return output_url

    def start_requests(self):

        id_list, name_list = InfoboxSpider.connect(self)
        urls = self.get_urls_fromDB(name_list)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        global id_dict
        parsed_uri = urlparse(response.url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        # print("checking url ======= ")
        # print(response.url)
        info_card = dict()
        name = str(response.url).replace("https://en.wikipedia.org/wiki/", "")

        rows = response.xpath('//*[@id="mw-content-text"]/div/table[@class="infobox vcard" ]/tbody/tr')

        for row in rows:

            # Scraping Image in info box
            value = dict()
            if row.css('.image'):
                pass

            # Scraping info box values
            elif row.xpath('th'):

                ## get the text value inside <th> and clean the format
                item = row.xpath('th//text()').extract()
                item = [_.strip() for _ in item if _.strip() and _.replace('\n', '')]
                item = ' '.join(item)
                item = item.replace('\n', '')
                item = unicodedata.normalize("NFKD", item)
                item = re.sub(r' +', ' ', item)
                item = item.strip()

                if row.xpath('td/div/ul/li'):
                    value = []
                    for li in row.xpath('td/div/ul/li'):
                        value.append(''.join(li.xpath('.//text()').extract()))
                    value = [_.strip() for _ in value if _.strip() and _.replace('\n', '')]
                    value = ', '.join(value)
                else:
                    value = row.xpath('td//text()').extract()
                    value = [_.strip() for _ in value if _.strip() and _.replace('\n', '')]

                    if item == 'Website':
                        value = ''.join(value)
                    else:
                        value = ' '.join(value)

                value = value.replace('\n', '')
                value = unicodedata.normalize("NFKD", value)
                value = re.sub(r' , ', ', ', value)
                value = re.sub(r' \( ', ' (', value)
                value = re.sub(r' \) ', ') ', value)
                value = re.sub(r' \)', ') ', value)
                value = re.sub(r'\[\d\]', ' ', value)
                value = re.sub(r' +', ' ', value)
                value = value.replace('"', '')
                value = value.strip()

                if item == "Location" or item == "Headquarters":
                    info_card[item] = InfoboxSpider.convert(self, item, value)

        info_card["id"] = id_dict[name]

        if "Location" not in info_card:
            info_card["Location"] = "null"

        if "Headquarters" not in info_card:
            info_card["Headquarters"] = "null"


        if len(info_card) > 3:
            yield {
                'Title': response.css('#firstHeading::text').extract_first(),
                'Organization_name': response.css('#mw-content-text > div >'
                                                  ' table.infobox.vcard > caption::text').extract_first(),
                **info_card
            }
