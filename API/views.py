from datetime import datetime
import json
import string
import random
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest, HttpResponseNotFound, HttpResponseRedirect
import json
from django.urls import reverse
from .models import Url

# TODO: what to do if there are query parameters in the url
def shortner_api(request: HttpRequest):
    body_unicode = request.body.decode('utf-8')
    params = dict(json.loads(body_unicode))
    response_data = {'massege': ''}
    DOMAIN = 'localhost:8000/api/short?url='        #can be imporved
    

    try:
        long_url = params.pop('url')
        long_url = long_url[0]
        if params:
            raise Exception
    except:
        response_data['massege'] = 'Bad request format'     
        return HttpResponseBadRequest(json.dumps(response_data))

    url_exists = Url.objects.filter(long_url=long_url).exists()

    if url_exists:
        response_data['massege'] = 'Success! returning an existent url'
        short_url = Url.objects.get(long_url=long_url).short_url
        response_data['short_url'] = DOMAIN + short_url
        response_data['is_new'] = False

    else:
        short_url = short_url_create()
        clicks = 0
        now = datetime.now()
        now = now.strftime("%Y/%m/%d %H:%M")
        url = Url(long_url=long_url, short_url=short_url,
                  clicks=clicks, time_created=now)
        url.save()
        response_data['massege'] = 'Success! returning a new url'
        response_data['short_url'] = DOMAIN + short_url
        response_data['is_new'] = True

    return HttpResponse(json.dumps(response_data))

# TODO: absolute path
def redirect_api(request: HttpRequest):
    params = dict(request.GET)
    response_data = {'massege': ''}

    try:
        short_url = params.pop('url')
        short_url = short_url[0]
        if params:
            raise Exception
    except:
        response_data['massege'] = 'Bad request format'
        return HttpResponseBadRequest(json.dumps(response_data))

    url_exists = Url.objects.filter(short_url=short_url).exists()

    if not url_exists:
        response_data['massege'] = 'Such short url does not exist'
        return HttpResponseNotFound(json.dumps(response_data))

    url = Url.objects.get(short_url=short_url)
    url.clicks += 1
    url.save()
    long_url = url.long_url
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
