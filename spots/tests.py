from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate
from django.contrib.gis.geos import Point
from django.core.files import File
from spots.models import Spot
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.


class TestSpotViews(APITestCase):

    def setUp(self):

        self.client = APIClient()

        self.example_spot = Spot(
            name = "Hammer Down Rail",
            coordinates = Point(0, 0)
        )

        self.example_spot.photo.save(
            'download.jpg',
            File(open('spots/tmp/download.jpg', 'rb'))
        )

        self.example_spot.save()

        self.example_user = User.objects.create_user(
            username = "username",
            email = "username@example.com",
            password = "password"
        )
        


    def test_list_spots(self):

        self.client.force_authenticate(user = self.example_user)

        response = self.client.get(
            reverse("spot-list")
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)


    
    def test_list_spots_near_user(self):

        self.client.force_authenticate(user = self.example_user)

        response = self.client.get("/v1/spots/", {"lat":"0", "lng":"0"})

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        


    def test_create_spot(self):

        self.client.force_authenticate(user = self.example_user)

        response = self.client.post(
            reverse("spot-list"),
            {
                "name": "280 Gap",
                "coordinates":{
                    "lng": 33.992393,
                    "lat": 86.999320
                },
            },
            format = "json"
        )

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)


    def test_update_spot(self):

        import os

        path_to_photo = os.path.join(os.getcwd(), "spots/tmp/download.jpg")

        self.client.force_authenticate(user = self.example_user)

        response = self.client.patch(
            reverse("spot-detail", args = [self.example_spot.id, ]),
            {
                "photo": open(path_to_photo, "rb")
            }
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)






