from django.conf.urls import url, include
from rest_framework_nested import routers
from rest_framework.authtoken import views as authviews

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'wishlists', views.WishlistViewSet, base_name='wishlists')

wishlist_router = routers.NestedSimpleRouter(router, r'wishlists', lookup='wishlist')
wishlist_router.register(r'item', views.ItemViewSet, base_name='wishlist_item')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(wishlist_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', authviews.obtain_auth_token)

]
