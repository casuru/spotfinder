from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
# Create your models here.


User = get_user_model()

class Spot(models.Model):

    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    name = models.CharField(max_length = 225)
    photo = models.ImageField(upload_to = 'spot_photos/')
    coordinates = models.PointField()


    def __str__(self):

        return self.user.username