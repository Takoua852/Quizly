from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class RegistrationTests(TestCase):
    """Test user registration endpoint."""

    def setUp(self):
        self.client = APIClient()

    def test_registration_success(self):
        """Register a new user successfully."""
        response = self.client.post("/api/register/", {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "confirmed_password": "testpass123"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_registration_password_mismatch(self):
        """Fail registration if passwords do not match."""
        response = self.client.post("/api/register/", {
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "pass1",
            "confirmed_password": "pass2"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_email_exists(self):
        """Fail registration if email already exists."""
        User.objects.create_user(username="existinguser", email="test3@example.com", password="pass123")
        response = self.client.post("/api/register/", {
            "username": "newuser",
            "email": "test3@example.com",
            "password": "pass123",
            "confirmed_password": "pass123"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(TestCase):
    """Test user login endpoint with JWT cookies."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="loginuser", email="login@example.com", password="pass123")

    def test_login_success(self):
        """Login successfully and set access/refresh cookies."""
        response = self.client.post("/api/login/", {
            "username": "loginuser",
            "password": "pass123"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)

    def test_login_invalid_credentials(self):
        """Fail login with wrong password."""
        response = self.client.post("/api/login/", {
            "username": "loginuser",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TokenRefreshTests(TestCase):
    """Test JWT token refresh endpoint using cookies."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="refreshuser", email="refresh@example.com", password="pass123")
        response = self.client.post("/api/login/", {"username": "refreshuser", "password": "pass123"})
        self.client.cookies = response.cookies

    def test_refresh_success(self):
        """Refresh access token successfully."""
        response = self.client.post("/api/token/refresh/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_missing_cookie(self):
        """Fail refresh if refresh token cookie is missing."""
        self.client.cookies.clear()
        response = self.client.post("/api/token/refresh/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutTests(TestCase):
    """Test user logout endpoint by deleting JWT cookies."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="logoutuser", email="logout@example.com", password="pass123")
        response = self.client.post("/api/login/", {"username": "logoutuser", "password": "pass123"})
        self.client.cookies = response.cookies

    def test_logout_success(self):
        """Logout user and delete JWT cookies."""
        response = self.client.post("/api/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.cookies.get("access_token").value, "")
        self.assertEqual(response.cookies.get("refresh_token").value, "")
