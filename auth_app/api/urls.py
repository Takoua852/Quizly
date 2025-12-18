"""
authentication_urls.py

Defines URL routing for user authentication endpoints including
registration, login with JWT cookies, token refresh, and logout.

Endpoints:
    - POST /register/          : Register a new user
    - POST /login/             : Login a user and set JWT access/refresh cookies
    - POST /logout/            : Logout a user and delete JWT cookies
    - POST /token/refresh/     : Refresh JWT access token using refresh token from cookie

Usage:
    Include this module in the project's main urls.py using Django's `include`.
"""
from django.urls import path
from .views import RegistrationView,CookieLogoutView,CookieLoginView,CookieTokenRefreshView


urlpatterns = [
    path('register/',RegistrationView.as_view(), name='register'),
    path('login/', CookieLoginView.as_view(), name="login"),
    path('logout/', CookieLogoutView.as_view(), name='logout'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]
