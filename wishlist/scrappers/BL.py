import urllib.request
import json
from bs4 import BeautifulSoup

from .data_scrap import standard_scrapping, steam_scrapping

headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


def check_site_type(url):
    for site in sites_dict.keys():
        if site in url:
            return site
    return 'standard'


def open_url(url):
    url_to_open = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(url_to_open) as url:
        return url.read()


def make_soup(url):
    page = open_url(url)
    return standard_scrapping(BeautifulSoup(page, 'html.parser'))


def make_json_for_steam(url):
    game_id = url.split('/app/')[1].split('/')[0]
    json_url = 'http://store.steampowered.com/api/appdetails?appids={0}'.format(game_id)
    game_data = json.loads(open_url(json_url))
    return steam_scrapping(game_data[game_id]['data'])


sites_dict = {
    'steam': make_json_for_steam,
    'standard': make_soup
}


def scrap(url):
    site_type = check_site_type(url)
    return sites_dict[site_type](url)


def refresh_price(url, price):
    site_type = check_site_type(url)

    pass

if __name__ == '__main__':
    scrap('http://store.steampowered.com/app/438490/GOD_EATER_2_Rage_Burst/')
