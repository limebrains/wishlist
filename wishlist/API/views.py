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

    @list_route(url_path='user')
    def user_wishlists(self, request, users=None):
        return Response(Wishlist.objects.filter(users=users))


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
