"""
authentication_views.py

Defines API endpoints for user registration, login with JWT stored in cookies,
token refresh, and logout for the authentication system.

Endpoints:
    - POST /register/         : Register a new user
    - POST /login/            : Login a user and set JWT access/refresh tokens in cookies
    - POST /token/refresh/    : Refresh JWT access token using refresh token from cookie
    - POST /logout/           : Logout a user and delete JWT cookies

Authentication:
    - Uses CookieJWTAuthentication for JWT stored in HTTP-only cookies
    - Some endpoints require authentication (IsAuthenticated)
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import RegistrationSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate
from .authentication import CookieJWTAuthentication


class RegistrationView(APIView):
    """
    API endpoint to register a new user.

    Permissions:
        - AllowAny

    HTTP methods:
        POST: Creates a new user from provided registration data.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request to register a new user.

        Args:
            request (Request): The HTTP request containing user data.

        Returns:
            Response: 201 Created if successful, 400 Bad Request with validation errors otherwise.
        """
        serializer = RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            serializer.save()
            data = {
                "detail": "User created successfully!"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookieLoginView(TokenObtainPairView):
    """
    API endpoint to login a user and issue JWT tokens via cookies.

    Permissions:
        - AllowAny

    Authentication:
        - CookieJWTAuthentication

    HTTP methods:
        POST: Returns user info and sets access/refresh JWT tokens as HTTP-only cookies.
    """
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for login.

        Args:
            request (Request): The HTTP request containing username/password.

        Returns:
            Response: 200 OK with user info if login successful; sets JWT cookies.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]

        response = Response(
            {"detail": "Login successfully!",
             "user": {
                 "id":  serializer.user.id,
                 "username": serializer.user.username,
                 "email": serializer.user.email,
             }
             }, status=status.HTTP_200_OK)

        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=True,
            samesite='Lax'
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response


class CookieTokenRefreshView(TokenRefreshView):
    """
    API endpoint to refresh the JWT access token using the refresh token stored in cookies.

    HTTP methods:
        POST: Refreshes the access token and updates the cookie.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to refresh JWT access token.

        Returns:
            Response: 200 OK with new access token, or 400/401 if refresh token is missing or invalid.
        """
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"detail": "Refresh token not found!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Refresh token invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        access_token = serializer.validated_data.get("access")
        response = Response({"detail": "Token refreshed",
                            "access": access_token}, status=status.HTTP_200_OK)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response


class CookieLogoutView(APIView):
    """
    API endpoint to logout a user by deleting JWT cookies.

    Permissions:
        - IsAuthenticated

    HTTP methods:
        POST: Deletes access and refresh cookies to logout the user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle POST request to logout a user.

        Returns:
            Response: 200 OK if cookies deleted successfully, 500 if an error occurs.
        """
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token:

                response = Response(
                    {"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."},
                    status=status.HTTP_200_OK
                )
                response.delete_cookie("access_token")
                response.delete_cookie("refresh_token")
                return response

        except Exception:
            return Response(
                {"detail": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
