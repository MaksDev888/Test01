from django.contrib.auth import authenticate

from .models import User
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    # def validate(self, attrs):
    #     user = authenticate(email=attrs.get('email'), password=attrs.get('password'))
    #     if user:
    #         return user
    #     return False


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]

    def save(self, **kwargs):
        user = User(email=self.validated_data["email"],
                    first_name=self.validated_data["first_name"],
                    last_name=self.validated_data["last_name"])
        user.set_password(self.validated_data["password"])
        user.save()
        return user
