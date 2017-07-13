import urllib.request
from bs4 import BeautifulSoup

data_to_gather = (
    ('title', 'og:title'),
    ('description', 'og:description'),
    ('site', 'og:site'),
    ('image', 'og:image'),
    ('price', 'twitter:data1'),
)

headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


def open_url(url):
    potential_request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(potential_request,) as url:
        return url.read()


def metatag_validation(data_property, soup):

    """
    Returns none if property doesn't exists.
    """

    metatag_property_names = ['property', 'name']
    for name in metatag_property_names:
        if not (soup.find("meta", attrs={name: data_property}) is None):
            return soup.find("meta", attrs={name: data_property})['content']

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
    pass
