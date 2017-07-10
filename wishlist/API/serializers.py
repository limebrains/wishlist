from rest_framework import serializers

from ..users.models import User
from .models import Wishlist


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class WishlistSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ('name', 'pk', 'description', 'date_created', 'owner', 'is_public')

