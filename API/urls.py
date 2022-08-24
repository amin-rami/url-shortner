from django.urls import path, include
from . import views


urlpatterns = [
    path('long', views.shortner_api),
    path('short', views.redirect_api)
]
