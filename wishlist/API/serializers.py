from rest_framework import serializers

from ..users.models import User
from .models import Wishlist, Item


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'username', 'email')


class WishlistSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer(read_only=True)
    users = UserSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ('name', 'pk', 'description', 'date_created', 'owner', 'is_public', 'users')

class ItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Item
        fields = ('name', 'pk', 'url', 'date_created', 'date_updated', 'raw_data', 'user_input')
        read_only_fields = ('raw_data',)
