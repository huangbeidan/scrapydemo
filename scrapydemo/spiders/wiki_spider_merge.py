import scrapy

class WikiSpider(scrapy.Spider):

    name = "wiki_company_merge"

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/Microsoft',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        strings = []
        for i in range(0, 100):
            try:
                for node in response.xpath('//*[@id="mw-content-text"]/div/p[{}]'.format(i)):
                    text = (node.xpath('string()').extract())
                    if len(text):
                        strings.append(text)
            except Exception as error:
                strings.append(str(error))


        rows = response.xpath("//*[@id='mw-content-text']/div/table[contains(@class, 'wikitable sortable')]/tbody/tr")
        table = {}
        for row in rows:
            columns = row.css('td')
            if(len(columns) == 3):
                company = columns[0].css('::text').extract_first()
                amount = columns[1].css('::text').extract_first()
                date = columns[2].css('::text').extract_first()

                table['company'] = company.strip()
                table['amount'] = amount.strip()
                table['date'] = date.strip()

                print(company, amount, date)

                yield{
                    **table
                }

                for next_page in row.css('td > a'):
                    yield response.follow(next_page, self.parse)

        yield{
             'Title': response.css('#firstheading::text').extract_first(),
            'Paragraphs': strings
        }


        return table
