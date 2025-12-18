"""
authentication.py

Defines a custom JWT authentication class that retrieves the access token
from HTTP-only cookies instead of the Authorization header.

Classes:
    - CookieJWTAuthentication: Extends rest_framework_simplejwt.authentication.JWTAuthentication
      to authenticate users using the 'access_token' cookie.
"""

from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that reads the JWT access token from cookies.

    Behavior:
        - Looks for the 'access_token' cookie in the incoming request.
        - Validates the token using SimpleJWT's built-in methods.
        - Returns a tuple of (user, validated_token) if authentication succeeds.
        - Returns None if the cookie is missing.

    Usage:
        Add this class to the `authentication_classes` of a DRF view or viewset:
            authentication_classes = [CookieJWTAuthentication]
    """
    def authenticate(self, request):
        """
        Authenticate the request using the 'access_token' cookie.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            tuple: (user, validated_token) if authentication succeeds.
            None: If no token is found in cookies.
        """
        raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        return user, validated_token
