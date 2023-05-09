from rest_framework import serializers

from .models import Friendship, FriendshipRequest, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class FriendshipSerializer(serializers.ModelSerializer):
    user_1 = UserSerializer()
    user_2 = UserSerializer()


    class Meta:
        model = Friendship
        fields = ('id', 'user_1', 'user_2')


class FriendshipRequestSerializer(serializers.ModelSerializer):
    addressee = UserSerializer()
    destination = UserSerializer()

    
    class Meta:
        model = FriendshipRequest
        fields = ('id', 'addressee', 'destination')
