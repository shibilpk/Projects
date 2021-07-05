from six import text_type
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(UserTokenObtainPairSerializer, cls).get_token(user)
        return token

    def validate(cls, attrs):

        data = super(UserTokenObtainPairSerializer, cls).validate(attrs)

        refresh = cls.get_token(cls.user)

        data['access'] = text_type(refresh.access_token)
        data['refresh'] = text_type(refresh)

        if cls.user.is_superuser:
            data['role'] = "superuser"
        else:
            data['role'] = "app_user"

        return data
