from bs4 import BeautifulSoup
import requests
import json

if __name__ == '__main__':


    url = 'https://www.linkedin.com/in/beidan/'
    response = requests.get(url, timeout=5)
    print(response)
    content = BeautifulSoup(response.content, "html.parser")
    print(content)
    # tweetArr = []
    # for tweet in content.findAll('div', attrs={"class": "tweetcontainer"}):
    #     tweetObject = {
    #         "author": tweet.find('h2', attrs={"class": "author"}).text.encode('utf-8'),
    #         "date": tweet.find('h5', attrs={"class": "dateTime"}).text.encode('utf-8'),
    #         "tweet": tweet.find('p', attrs={"class": "content"}).text.encode('utf-8'),
    #         "likes": tweet.find('p', attrs={"class": "likes"}).text.encode('utf-8'),
    #         "shares": tweet.find('p', attrs={"class": "shares"}).text.encode('utf-8')
    #     }
    #     tweetArr.append(tweetObject)
    # with open('twitterData.json', 'w') as outfile:
    #     json.dump(tweetArr, outfile)