import datetime
from celery import Celery
from wishlist.api.models import Item
from wishlist.scrappers.bl import scrap

app = Celery()

@app.task
def get_item_raw_data(pk):
    print("Invoked get_item for {}".format(pk))
    item = Item.objects.get(pk=pk)
    item.raw_data = scrap(item.url)
    item.save()


@app.task
def update_price():
    time_threshold = datetime.datetime.now() - datetime.timedelta(minutes=5)

    items = Item.objects \
                .exclude(raw_data__contains={'price': None}) \
                .filter(date_updated__lt=time_threshold) \
                .order_by('date_updated')[:10]

    countdown = 0
    for item in items:
        get_item_raw_data.apply_async((item.pk,), countdown=countdown, routing_key='item.update')
        countdown += 2


class Router(object):

    def route_for_task(self, task, args=None, kwargs=None):
        if task == "item.update":
            return "periodic.tasks"
        if task == "item.new":
            return "task.item.new"
        else:
            return "default"
