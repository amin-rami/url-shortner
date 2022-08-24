from django.urls import path, include
from . import views


urlpatterns = [
    path('long', views.shortner_api, name='long'),
    path('short/<short_url>', views.redirect_api, name='short')
]
