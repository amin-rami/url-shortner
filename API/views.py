from datetime import datetime, timedelta
import json
import string
import random
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from .models import Url
from rest_framework.decorators import api_view
from .urls import urlpatterns 

time_diff = timedelta(hours=4, minutes = 30)

@api_view(['POST', 'GET'])
def shortner_api(request: HttpRequest):

    body_unicode = request.body.decode('utf-8')
    params = dict(json.loads(body_unicode))
    response_data = {'message': ''}
    DOMAIN = 'localhost:8000/api/short/'  # can be imporved

    try:
        long_url = params.pop('url')
        if params:
            raise Exception
    except:
        response_data['message'] = 'Bad request format'
        return HttpResponseBadRequest(json.dumps(response_data))

    short_url = short_url_create()
    clicks = 0
    now = datetime.now() + time_diff
    now = now.strftime("%Y/%m/%d %H:%M")
    url = Url(long_url=long_url, short_url=short_url,
              clicks=clicks, time_created=now)
    url.save()
    response_data['message'] = 'Success!'
    response_data['short_url'] = DOMAIN + short_url

    return HttpResponse(json.dumps(response_data))


@api_view(['POST', 'GET'])
def redirect_api(request: HttpRequest, short_url):
    response_data = {'message': ''}

    url_exists = Url.objects.filter(short_url=short_url).exists()

    if not url_exists:
        response_data['message'] = 'Such short url does not exist'
        return HttpResponseNotFound(json.dumps(response_data))

    url = Url.objects.get(short_url=short_url)
    url.clicks += 1
    now = datetime.now() + time_diff
    now = now.strftime("%Y/%m/%d %H:%M")
    url.last_access = now
    url.save()
    long_url = url.long_url
    if not ('http://' in long_url or 'https://' in long_url):
        long_url = 'http://' + long_url
    return HttpResponseRedirect(long_url)


def short_url_create():
    char_set = string.ascii_lowercase + string.ascii_uppercase
    MAX_LEN = 6

    while True:
        short_url = ''
        length = random.choice(range(1, MAX_LEN+1))
        for i in range(length):
            short_url += random.choice(char_set)

        url_exists = Url.objects.filter(short_url=short_url).exists()
        if not url_exists:
            break

    return short_url
