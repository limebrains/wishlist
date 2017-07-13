def steam_scrapping(game_data):
    data_to_gather = (
        ('title', 'name'),
        ('description', 'about_the_game'),
        ('image', 'background'),
        ('price', 'price_overview')
    )
    raw_data = {}
    raw_data['site'] = 'steam'

    for name, property in data_to_gather:
        raw_data[name] = game_data[property]

    return raw_data


def standard_scrapping(soup):
    data_to_gather = (
        ('title', 'og:title'),
        ('description', 'og:description'),
        ('site', 'og:site'),
        ('image', 'og:image'),
        ('price', 'twitter:data1'),
    )

    raw_data = {}

    for data_name, data_property in data_to_gather:
        raw_data[data_name] = standard_metatag_validation(data_property, soup)

    return raw_data


def standard_metatag_validation(data_property, soup):

    """
    Returns none if property doesn't exists.
    """

    metatag_property_names = ['property', 'name']
    for name in metatag_property_names:
        if not (soup.find("meta", attrs={name: data_property}) is None):
            return soup.find("meta", attrs={name: data_property})['content']

    return None


if __name__ == '__main__':
    pass
