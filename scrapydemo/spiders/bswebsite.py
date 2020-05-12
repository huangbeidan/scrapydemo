

if __name__ == "__main__":
    from requests import get
    url = 'http://www.google.com/search?q=California+State+University+Fresno'
    response = get(url)

    from bs4 import BeautifulSoup

    html_soup = BeautifulSoup(response.text, 'html.parser')
    print(html_soup)

    #print(type(html_soup))

    movie_containers = html_soup.find_all('div', class_='mod')
    # print((movie_containers))
