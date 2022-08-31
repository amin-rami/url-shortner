from django.contrib import admin
from .models import Url


class URLAdmin(admin.ModelAdmin):
    list_display = ['id', 'long_url', 'short_url', 'desktop_clicks', 'mobile_clicks',
                    'clicks', 'time_created', 'last_access', 'owner']


admin.site.register(Url, URLAdmin)
