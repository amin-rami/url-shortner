import json, string, random
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
import json
from .models import Url


def shortner_api(request: HttpRequest):
    params = dict(request.GET)
    response_data = {'massege': ''}

    try:
        long_url = params.pop('url')
        if params:
            raise Exception
    except:
        response_data['massege'] = 'Bad request format'
        return HttpResponseBadRequest(json.dumps(response_data))

    url_exists = Url.objects.filter(long_url=long_url).exists()

    if url_exists:
        response_data['massege'] = 'Success! returning an existent url'
        short_url = Url.objects.get(long_url=long_url).short_url
        response_data['short_url'] = short_url
        response_data['is_new'] = False
        return HttpResponse(json.dumps(response_data))

    else:
        pass

    return HttpResponse('Success!')


def redirect_api(requset: HttpRequest):
    pass


def short_url_create(long_url):
    char_set = string.ascii_lowercase + string.ascii_uppercase
    MAX_LEN = 6

    while True:
        short_url = ''
        length = random.choice(range(1, MAX_LEN+1))
        for i in range(length):
            short_url += random.choice(char_set)
        
        url_exists = Url.objects.filter(short_url = short_url).exists()
        if not url_exists:
            break
    
    return short_url


