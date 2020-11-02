from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.contrib.auth import get_user_model
User = get_user_model()



class TestUserViews(APITestCase):


    def setUp(self):

        self.example_user = User.objects.create_user(
            username = "username",
            email = "username@example.com",
            password = "password"
        )

        self.client = APIClient()

    
    def test_create_user(self):

        response = self.client.post(
            reverse("user-list"),
            {
                "username":"example",
                "email":"example@example.com",
                "password":"password",
                "confirm_password": "password"
            }
        )

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)

    
    def test_create_user_requires_confirm_password(self):

        response = self.client.post(
            reverse("user-list"),
            {
                "username":"example",
                "email":"example@example.com",
                "password":"password",
            }
        )

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)


    def test_create_user_requires_passwords_match(self):

        response = self.client.post(
            reverse("user-list"),
            {
                "username": "example",
                "email":"example@example.com",
                "password": "password",
                "confirm_password":"different"
            }
        )

        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)