from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for register
    """
    password = serializers.CharField(max_length=70, min_length=6, write_only=True)
    email = serializers.EmailField(max_length=70, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', None)
        if User.objects.filter(email=email):
            raise serializers.ValidationError("This email already exists")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer for login
    """
    password = serializers.CharField(max_length=70, min_length=6, write_only=True)
    email = serializers.EmailField(max_length=70)
    tokens = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid email or password, try again")

        result = {
            'email': user.email,
            'tokens': user.tokens(),
        }

        return result
