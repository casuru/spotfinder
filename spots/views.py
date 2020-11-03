from rest_framework import viewsets
from spots.serializers import SpotSerializer
from spots.models import Spot
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class SpotViewSet(viewsets.ModelViewSet):

    serializer_class = SpotSerializer
    queryset = Spot.objects.all()
    permission_classes = (IsAuthenticated, )


    def perform_create(self, serialized_spot):

        serialized_spot.save(user = self.request.user)
