from celery import Celery
from ..scrappers.bl import refresh_price, scrap
from .models import Item

app = Celery()


@app.task
def add_item(url):
    return scrap(url)


@app.task
def update_price():
    items = Item.filter(price__isnull = False)
    print(items)
    for item in items:
        refresh_price(item.url, item.raw_data['price'])


@app.task
def test(arg):
    print(arg)
