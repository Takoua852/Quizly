"""URL routing for user authentication endpoints."""

from django.urls import path
from .views import RegistrationView,CookieLogoutView,CookieLoginView,CookieTokenRefreshView


urlpatterns = [
    path('register/',RegistrationView.as_view(), name='register'),
    path('login/', CookieLoginView.as_view(), name="login"),
    path('logout/', CookieLogoutView.as_view(), name='logout'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]
