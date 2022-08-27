from datetime import datetime, timedelta
from genericpath import exists
import json
import string
import random
from urllib import request, response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from .models import Url
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
import django.contrib.auth
from django.contrib.auth.middleware import AuthenticationMiddleware


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


@api_view(['POST', 'GET'])
def signup_api(request):

    body_unicode = request.body.decode('utf-8')
    params = dict(json.loads(body_unicode))
    response_data = {'message': ''}

    try:
        username = params.pop('username')
        password = params.pop('password')
        if params:
            raise Exception
    except:
        response_data['message'] = 'Bad request format'
        return HttpResponseBadRequest(json.dumps(response_data))

    exists = User.objects.filter(username=username).exists()
    if exists:
        response_data['message'] = 'Username already exists'
        return HttpResponse(json.dumps(response_data))
    
    user = User.objects.create_user(username=username, password=password)
    user.save()

    response_data['message'] = f'Success! {username}, welcome to our website'
    return HttpResponse(json.dumps(response_data))

@api_view(['POST', 'GET'])
def login_api(request):
    logout(request)
    body_unicode = request.body.decode('utf-8')
    params = dict(json.loads(body_unicode))
    response_data = {'message': ''}

    try:
        username = params.pop('username')
        password = params.pop('password')
        if params:
            raise Exception
    except:
        response_data['message'] = 'Bad request format'
        return HttpResponseBadRequest(json.dumps(response_data))


    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        response_data['message'] = f'Logged in successfully! Welcome back, {user.get_username()}' #add user's name
        return HttpResponse(json.dumps(response_data))
    
    else:
        response_data['message'] = 'Incorrect username or password'
        return HttpResponse(json.dumps(response_data))


@api_view(['POST', 'GET'])
def logout_api(request: HttpRequest):
    logout(request)
    response_data = {'message': 'Successfully logged out!'}
    return HttpResponse(json.dumps(response_data))

@api_view(['POST', 'GET'])
def is_logged(requset: HttpRequest):
    if requset.user.is_authenticated:
        return HttpResponse(f'{requset.user.get_username()}')
    else:
        return HttpResponse('Not logged')


