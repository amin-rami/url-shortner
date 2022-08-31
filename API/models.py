from django.db import models
from django.contrib.auth.models import User


class Url(models.Model):
    id = models.AutoField(primary_key=True)
    long_url = models.CharField(max_length=500)
    short_url = models.CharField(max_length=500)
    mobile_clicks = models.IntegerField(blank=True, default=0)
    desktop_clicks = models.IntegerField(blank=True, default=0)
    clicks = models.IntegerField(blank=True)
    time_created = models.CharField(max_length=100)
    last_access = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        s = f'long_url: {self.long_url}     short_url: {self.short_url}        clicks: {self.clicks}       time created: {self.time_created}'
        return s





