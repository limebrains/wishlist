from rest_framework import serializers

from ..users.models import User
from .models import Wishlist, Item


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser',)
        fields = ('pk', 'username', 'email', 'is_staff', 'is_superuser',)

    def update(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        user.set_password(attrs['password'])
        return user

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user



class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'pk', 'url', 'date_created', 'date_updated', 'raw_data', 'user_input')
        read_only_fields = ('raw_data',)


class WishlistSerializer(serializers.HyperlinkedModelSerializer):
    owner = UserSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)
    items = ItemSerializer(read_only=True, many=True,)

    class Meta:
        model = Wishlist
        fields = ('name', 'pk', 'description',
                  'date_created', 'date_updated',
                  'owner', 'is_public',
                  'users', 'items')


