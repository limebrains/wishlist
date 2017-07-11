from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from django.db.models import Q

from ..users.models import User
from .permissions import IsOwnerOrReadOnly
from .serializers import WishlistSerializer, UserSerializer
from .models import Wishlist


class WishlistFilter(filters.FilterSet):
    class Meta:
        model = Wishlist
        fields = ('name', 'users')


class FilterableMixin:
    filter_backends = [DjangoFilterBackend, ]


class WishlistViewSet(FilterableMixin, viewsets.ModelViewSet):
    filter_class = WishlistFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(
            Q(users=self.request.user) | Q(is_public=True)
        ).distinct()


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(FilterableMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
