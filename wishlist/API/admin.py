from django.contrib import admin
from .models import Wishlist, Item


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    exclude = ('date_created', 'date_updated', 'slug')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    exclude = ('date_created', 'date_updated', 'raw_data')
