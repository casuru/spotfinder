from rest_framework import viewsets
from spots.serializers import SpotSerializer
from spots.models import Spot
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

# Create your views here.


class SpotViewSet(viewsets.ModelViewSet):

    serializer_class = SpotSerializer
    permission_classes = (IsAuthenticated, )


    def get_queryset(self):

        lat = self.request.query_params.get("lat", None)
        lng = self.request.query_params.get("lng", None)

        if lat and lng:

            user_location = Point(
                float(lng), 
                float(lat)
            )

            spots = Spot.objects.filter(coordinates__distance_lte = (user_location, 1000))

            return spots
        
        return Spot.objects.all()



    def perform_create(self, serialized_spot):

        serialized_spot.save(user = self.request.user)
