from django.db import models


class Url(models.Model):
    id = models.AutoField(primary_key=True)
    long_url = models.CharField(max_length=500)
    short_url = models.CharField(max_length=500)
    clicks = models.IntegerField()
    time_created = models.CharField(max_length=100)
    last_access = models.CharField(max_length=100, blank=True)
    owner = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        s = f'long_url: {self.long_url}     short_url: {self.short_url}        clicks: {self.clicks}       time created: {self.time_created}'
        return s





