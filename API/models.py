from django.db import models


class Url(models.Model):
    long_url = models.CharField(max_length=500, primary_key=True)
    short_url = models.CharField(max_length=500)
    clicks = models.IntegerField()
    time_created = models.CharField(max_length=100)

    