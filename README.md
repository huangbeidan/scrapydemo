# scrapydemo

## Tool 1: WikiPedia Infobox Scrapper
This tool will take a list of company names as input, and return the infomation in Wikipedia as both Json and CSV.

Just run in terminal:
cd to scrapydemo/scrapydemo
scrapy crawl infobox_spider -o info-result.json

If you need to convert the JSON into csv:
run json2csvTool.py
