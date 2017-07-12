import urllib.request
from bs4 import BeautifulSoup

data_to_gather = (
    ('title', 'og:title'),
    ('description', 'og:description'),
    ('site', 'og:site'),
    ('image', 'og:image'),
    ('price', 'twitter:data1'),
)


def open_url(url):
    potential_request = urllib.request.Request(url)
    with urllib.request.urlopen(potential_request) as url:
        return url.read()


def metatag_validation(data_property, soup):

    if not (soup.find("meta", attrs={'property': data_property}) is None):
        return soup.find("meta", attrs={'property': data_property})['content']

    if not (soup.find("meta", attrs={'name': data_property}) is None):
        return soup.find("meta", attrs={'name': data_property})['content']

    return None


def soup_scrapping(soup):
    raw_data = {}

    for data_name, data_property in data_to_gather:
        raw_data[data_name] = metatag_validation(data_property, soup)

    return raw_data


def scrap(url):
    page = open_url(url)
    return soup_scrapping(BeautifulSoup(page, 'html.parser'))


if __name__ == '__main__':
    print(
    scrap('http://allegro.pl/technorattan-meble-ogrodowe-komplet-dla-4' +
          '-asturito-i6847244478.html?sh_dwh_token=d0b6dd74a8394345128e20d296cb1c5e')
    )
