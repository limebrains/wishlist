from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework import viewsets, renderers, permissions
from rest_framework.decorators import list_route

from ..users.models import User
from .permissions import IsOwnerOrReadOnly
from .serializers import WishlistSerializer, UserSerializer
from .models import Wishlist


class WishlistViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Wishlist.objects.filter(users=self.request.user)

    serializer_class = WishlistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None
