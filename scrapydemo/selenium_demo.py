import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


page_url = "https://www.linkedin.com/in/beidan/"


driver = webdriver.Chrome('/Users/beidan/scrapydemo/scrapydemo/chromedriver')

profile_list = []

driver.find_elements(By.XPATH, '//*[@id="ember1826"]/div')

# for company in company_list:
#     driver.get(page_url)
#     searchBox = driver.find_element_by_id("keyword_m")
#     searchBox.send_keys(company)
#     driver.find_element_by_xpath("/html/body/div[1]/article/section[1]/div/form/div/div[2]/input").click()
#     companyCode = driver.find_element_by_xpath("//*[@id='result-naics']/ul/li/a/div").text
#     print(companyCode)
#     time.sleep(2)
