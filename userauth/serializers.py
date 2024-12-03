from rest_framework import serializers
from .models import UserProfile


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         # fields = ['id', 'user', 'phone_number', 'address']
#         fields = '__all__'
#         depth = 1  # Hozzáadja a kapcsolódó `User` adatait is
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'phone_number', 'address')
