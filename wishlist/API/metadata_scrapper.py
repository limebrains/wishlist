import urllib.request
from bs4 import BeautifulSoup

data_to_gather = (
    ('title', 'og:title'),
    ('description', 'og:description'),
    ('url', 'og:url'),
    ('site', 'og:site'),
    ('price', 'twitter:data1'),
)


def open_url(url):
    potential_request = urllib.request.Request(url)
    with urllib.request.urlopen(potential_request) as url:
        return url.read()


def soup_scrapping(soup):
    raw_data = {}

    for data_name, data_property in data_to_gather:
        try:
            raw_data[data_name] = soup.find("meta", property=data_property)['content']
        except TypeError:
            raw_data[data_name] = soup.find("meta", attrs={'name': data_property})['content']

    return raw_data


def scrap(url):
    page = open_url(url)
    return soup_scrapping(BeautifulSoup(page, 'html.parser'))


if __name__ == '__main__':
    print(scrap(
        'https://www.zalando.pl/' +
        'levi-s-the-perfect-t-shirt-z-nadrukiem-le221d022-a12.html'
    ))
