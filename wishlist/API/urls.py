from django.conf.urls import url, include
from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
router.register(r'wishlists', views.WishlistViewSet, base_name='wishlists')

wishlist_router = routers.NestedSimpleRouter(router, r'wishlists', lookup='wishlist')
wishlist_router.register(r'item', views.ItemViewSet, base_name='wishlist_item')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(wishlist_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
