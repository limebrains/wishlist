import datetime
from celery import current_app
from wishlist.api.models import Item
from wishlist.scrappers.bl import scrap

app = current_app

@app.task()
def get_item_raw_data(pk):
    item = Item.objects.get(pk=pk)
    item.raw_data = scrap(item.url)
    item.save()


@app.task()
def update_price():
    time_threshold = datetime.datetime.now() - datetime.timedelta(minutes=2)
    items = Item.objects \
                .exclude(raw_data__contains={'price': None}) \
                .filter(date_updated__lt=time_threshold) \
                .order_by('date_updated')[:10]

    countdown = 0
    for item in items:
        get_item_raw_data.apply_async((item.pk,), countdown=countdown)
        countdown += 2
