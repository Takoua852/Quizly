"""
authentication_serializers.py

Defines serializers for user registration and JWT authentication.

Serializers:
    - RegistrationSerializer: Handles user creation with password confirmation
      and email uniqueness validation.
    - CustomTokenObtainPairSerializer: Extends SimpleJWT's TokenObtainPairSerializer
      to validate username and password and return JWT tokens.
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Fields:
        - username: Required, unique identifier for the user
        - password: Required, write-only
        - confirmed_password: Required, write-only, must match password
        - email: Required, must be unique

    Validations:
        - Password and confirmed_password must match
        - Email must not already exist in the database

    Usage:
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
    """
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirmed_password', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

    def validate(self, data):
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."})
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        """
        Create and save a new User instance with a hashed password.

        Returns:
            User: The newly created user instance
        """
        pw = self.validated_data['password']

        account = User(
            email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining JWT token pair (access and refresh).

    Extends TokenObtainPairSerializer to:
        - Validate username exists
        - Validate password is correct
        - Return JWT tokens if authentication succeeds

    Usage:
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data
    """


    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid username or password")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid username or password")

        data = super().validate({
            "username": user.username,
            "password": password
        })

        self.user = user
        return data