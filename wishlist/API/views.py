from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from django.db.models import Q
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from ..users.models import User
from .permissions import IsOwnerOrReadOnly
from .serializers import WishlistSerializer, UserSerializer, ItemSerializer
from .models import Wishlist, Item


class WishlistFilter(filters.FilterSet):
    class Meta:
        model = Wishlist
        fields = ('name', 'description', 'users')


class ItemFilter(filters.FilterSet):
    class Meta:
        model = Item
        fields = ('name', 'url')


class FilterableMixin:
    filter_backends = [DjangoFilterBackend, ]


class WishlistViewSet(FilterableMixin, viewsets.ModelViewSet):
    filter_class = WishlistFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    serializer_class = WishlistSerializer

    def get_queryset(self):
        qs = Wishlist.objects.filter(
            (Q(users=self.request.user) & Q(is_public=False))
            |
            (Q(is_public=True))
        ).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user,
                        users=[self.request.user, ])


class ItemViewSet (FilterableMixin, viewsets.ModelViewSet):
    filter_class = ItemFilter
    serializer_class = ItemSerializer

    def get_queryset(self,):
        query = Item.objects.filter(wishlist=self.kwargs['wishlist_pk'])
        return query

    def perform_create(self, serializer):
        serializer.save(wishlist_id=self.kwargs['wishlist_pk'])


class UserViewSet(FilterableMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None

    @list_route(methods=['get'], permission_classes=[IsOwnerOrReadOnly], url_path='get-username')
    def get_username(self, request):
        return Response(UserSerializer(self.request.user).data)
