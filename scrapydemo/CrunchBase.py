import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


page_url = "https://www.youtube.com/watch?v=HwCIDG-ahp0"


driver = webdriver.Chrome()
driver.get(page_url)
time.sleep(2)


title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
print(title)


SCROLL_PAUSE_TIME = 2
CYCLES = 2

html = driver.find_element_by_tag_name('html')
html.send_keys(Keys.PAGE_DOWN)
html.send_keys(Keys.PAGE_DOWN)
time.sleep(SCROLL_PAUSE_TIME * 3)

for i in range(CYCLES):
    html.send_keys(Keys.END)
    time.assleep(SCROLL_PAUSE_TIME)
    print(i)

comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
all_comments = [elem.text for elem in comment_elems]
print(all_comments)

replies_elems =driver.find_elements_by_xpath('//*[@id="replies"]')
all_replies = [elem.text for elem in replies_elems]
print(all_replies)

write_file = "output_replies.csv"
with open(write_file, "w") as output:
    for line in all_replies:
        output.write(line + '\n')