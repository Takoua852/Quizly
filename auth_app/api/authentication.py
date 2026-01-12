"""
authentication.py

Defines a custom JWT authentication class that retrieves the access token
from HTTP-only cookies instead of the Authorization header.

Classes:
    - CookieJWTAuthentication: Extends rest_framework_simplejwt.authentication.JWTAuthentication
      to authenticate users using the 'access_token' cookie.
"""

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class CookieJWTAuthentication(JWTAuthentication):
    """Authenticate users using the JWT access token stored in cookies."""

    def authenticate(self, request):
        """Return (user, token) from the 'access_token' cookie or None."""

        raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError):
            raise AuthenticationFailed("Invalid or expired access token")

        user = self.get_user(validated_token)
        return user, validated_token
