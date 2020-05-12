from urllib.parse import urlparse
import scrapy

from scrapy.http import Request

class pwc_tax(scrapy.Spider):
    name = "pwc_tax"

    allowed_domains = ["crsreports.congress.gov"]
    start_urls = ["https://crsreports.congress.gov/search/#/0?termsToSearch=&orderBy=Date&navIds=4294964442"]


    def parse(self, response):
        base_url = "https://crsreports.congress.gov/search/#/0?termsToSearch=&orderBy=Date&navIds=4294964442"
        for a in response.xpath('//a[@href]/@href'):
            link = a.extract()

            if link.endswith('.pdf'):
                link = base_url + link
                self.logger.info(link)
                yield Request(link, callback=self.save_pdf)

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        with open(path, 'wb') as f:
            f.write(response.body)