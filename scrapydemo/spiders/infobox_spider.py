from configparser import ConfigParser
from urllib.parse import urlparse

import psycopg2
import scrapy

# -*- coding: utf-8 -*-

import scrapy
import re
import unicodedata
from scrapy.crawler import CrawlerProcess

from configparser import ConfigParser
from configdb import configdb

class InfoboxSpider(scrapy.Spider):
    name = 'infobox_spider'

    from configparser import ConfigParser
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
        try:
            # read connection parameters
            params = configdb()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            # create a cursor
            cur = conn.cursor()

            # execute a statement
            cur.execute('select distinct name from patentassignees;')

            # display the PostgreSQL database server version
            db_version = cur.fetchall()
            name_list = [tuple[0] for tuple in db_version]

            # close the communication with the PostgreSQL
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')
                return name_list

    # start_urls = ['https://en.wikipedia.org/wiki/Instagram']

    # Two ways of getting URLS
    def get_urls(self):
        lines = [line.rstrip() for line in open("defense-company-list.tsv")]
        companylist = []


        for i in range(len(lines)):
            if(i==0):
                continue
            value = re.split(r'\t', lines[i])
            if(len(value)==2):
                cleaned = value[1].replace(" ","_")
                cleaned = re.sub(r"\(.*\)", "", cleaned)
                companylist.append(cleaned)
        output_url = ["https://en.wikipedia.org/wiki/" + x for x in companylist]
        return output_url

    def get_urls_fromDB(self, lines):

        companylist = []
        for i in range(len(lines)):
                cleaned = lines[i].replace(" ","_")
                cleaned = re.sub(r"\(.*\)", "", cleaned)
                companylist.append(cleaned)
        output_url = ["https://en.wikipedia.org/wiki/" + x for x in companylist]
        return output_url


    def start_requests(self):
        urls = self.get_urls()

        #name_list = InfoboxSpider.connect(self)
        #urls = self.get_urls_fromDB(name_list)
        #print("urls are" + str(urls))

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
        for i in range(0, 100):
            try:
                for node in response.xpath('//*[@id="mw-content-text"]/div/p[{}]'.format(i)):
                    text = _clean(node.xpath('string()').extract())
                    if len(text):
                        strings.append(text)
            except Exception as error:
                strings.append(str(error))
        info_card = dict()
        i = 0
        rows = response.xpath('//*[@id="mw-content-text"]/div/table[@class="infobox vcard" ]/tbody/tr')

        for row in rows:

            # Scraping Image in info box
            value = dict()
            if row.css('.image'):
                if row.css('img'):
                    i += 1
                    item = 'Logo_{}'.format(i)
                    try:
                        value['logo_thumb_url'] = row.css('img').xpath('@src').extract_first().replace('//', '')
                        try:
                            value['logo_url'] = domain + row.css('a::attr(href)').extract_first()[1:]
                            try:
                                text = _clean(row.xpath('string()').extract())
                                if text:
                                    value['text'] = text
                            except:
                                pass
                        except:
                            pass
                    except:
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

                # convert string list into list of strings
                # info_card[item] = InfoboxSpider.convert(item, value)
                # InfoboxSpider.convert(self, item, value)
                info_card[item] = InfoboxSpider.convert(self, item, value)
        # print(info_card)
        # print("received")

        if len(info_card) > 0:
            yield {
                'Title': response.css('#firstHeading::text').extract_first(),
                'Organization_name': response.css('#mw-content-text > div >'
                                                  ' table.infobox.vcard > caption::text').extract_first(),
                **info_card
            }
