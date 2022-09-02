from django.urls import path, include
from . import views


urlpatterns = [
    path('long', views.shortner_api, name='long'),
    path('short/<short_url>', views.redirect_api, name='short'),
    path('users/login', views.login_api),
    path('users/logout', views.logout_api),
    path('users/signup', views.signup_api),
    path('users/status', views.status),
    path('users/edit', views.edit),
    path('users/myurls', views.my_urls),
    path('docs', views.docs)
]
