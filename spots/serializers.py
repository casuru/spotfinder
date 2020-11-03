from rest_framework import serializers
from spots.models import Spot
from django.contrib.gis.geos import Point

class PointField(serializers.Field):


    def to_representation(self, value):

        return {
            "lng": value.coordinates[0],
            "lat": value.coordinates[1]
        }


    def to_internal_value(self, data):

        

        point = Point(
            data["lng"],
            data["lat"]
        )

        return {"coordinates": point}


class SpotSerializer(serializers.ModelSerializer):

    coordinates = PointField(source = "*")

    class Meta:

        model = Spot
        fields = "__all__"
        extra_kwargs = {
            "user":{
                "read_only": True
            },
            "photo":{
                "required": False
            }
        }