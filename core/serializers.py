from django.contrib.auth import authenticate
from rest_framework import serializers
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=200, required=True)

    def create(self, data):
        return data
    
    def validate(self, data):
        email = data['email']
        password = data['password']
        try:
            auth = authenticate(email=email, password=password)
            if auth is None:
                raise serializers.ValidationError(f"Invalid login details")
        except User.DoesNotExist:
            raise serializers.ValidationError(f"User with email {email} does not exist")
        return data
