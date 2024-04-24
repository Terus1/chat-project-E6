from django.contrib.auth.models import User


from requests import Response
from rest_framework import serializers

from .models import Room, Message, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RoomSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'slug', 'members']

    def delete(self, request, *args, **kwargs):
        room = self.get_object()
        room.delete()
        return Response({'success': True})


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Message
        fields = ['id', 'room', 'user', 'text', 'date_added']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'picture']
