from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

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
