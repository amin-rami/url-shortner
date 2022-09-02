from asyncore import read
from datetime import datetime, timedelta
import json
import string
import random
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Url
from rest_framework.request import Request
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.middleware.common import CommonMiddleware
from django.views.decorators.csrf import csrf_exempt
import re
from ipware import get_client_ip

time_diff = timedelta(hours=4, minutes=30)


def method_check(request: HttpRequest, allowed):
    method = request.method
    if method == allowed:
        return True
    return False


@csrf_exempt
def shortner_api(request: HttpRequest):
    response_data = {}
    allowed_method = 'POST'
    if not method_check(request, allowed_method):
        response_data['message'] = 'Request method not allowed'
        return JsonResponse(response_data, status=405)

    params = dict(request.POST)
    unpack(params)
    response_data = {'message': ''}
    DOMAIN = 'localhost:8000/api/short/'  # can be imporved

    try:
        long_url = params.pop('url')
        if params:
            raise Exception
    except:
        response_data['message'] = 'Bad request format'
        return JsonResponse(response_data, status=400)

    if request.user.is_authenticated:
        user = request.user
        exists = Url.objects.filter(long_url=long_url, owner=user).exists()
        if exists:
            response_data['message'] = 'Success!'
            short_url = Url.objects.get(
                long_url=long_url, owner=user).short_url
            response_data['short_url'] = DOMAIN + short_url

        else:
            clicks = 0
            short_url = short_url_create()
            now = datetime.now() + time_diff
            now = now.strftime("%Y/%m/%d %H:%M")
            url = Url(long_url=long_url, short_url=short_url,
                      clicks=clicks, time_created=now, owner=user)
            url.save()
            response_data['message'] = 'Success!'
            response_data['short_url'] = DOMAIN + short_url

    else:
        short_url = short_url_create()
        clicks = 0
        now = datetime.now() + time_diff
        now = now.strftime("%Y/%m/%d %H:%M")
        url = Url(long_url=long_url, short_url=short_url,
                  clicks=clicks, time_created=now)
        url.save()
        response_data['message'] = 'Success!'
        response_data['short_url'] = DOMAIN + short_url

    return JsonResponse(response_data)


@csrf_exempt
def redirect_api(request: Request, short_url):
    response_data = {}
    allowed_method = 'GET'
    if not method_check(request, allowed_method):
        response_data['message'] = 'Request method not allowed'
        return JsonResponse(response_data, status=405)

    response_data = {'message': ''}
    url_exists = Url.objects.filter(short_url=short_url).exists()

    if not url_exists:
        response_data['message'] = 'Such short url does not exist'
        return JsonResponse(response_data, status=404)

    url = Url.objects.get(short_url=short_url)
    if mobile(request):
        url.mobile_clicks += 1
    else:
        url.desktop_clicks += 1
    url.clicks += 1
    now = datetime.now() + time_diff
    now = now.strftime("%Y/%m/%d %H:%M")
    url.last_access = now
    url.save()
    long_url = url.long_url
    if not ('http://' in long_url or 'https://' in long_url):
        long_url = 'http://' + long_url
    print(long_url)
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


@csrf_exempt
def signup_api(request):
    response_data = {}
    allowed_method = 'POST'
    if not method_check(request, allowed_method):
        response_data['message'] = 'Request method not allowed'
        return JsonResponse(response_data, status=405)

    params = dict(request.POST)
    unpack(params)
    response_data = {'message': ''}

    try:
        username = params.pop('username')
        password = params.pop('password')
        if params:
            raise Exception
    except:
        response_data['message'] = 'Bad request format'
        return JsonResponse(response_data, status=400)

    exists = User.objects.filter(username=username).exists()
    if exists:
        response_data['message'] = 'Username already exists'
        return JsonResponse(response_data, status=403)

    user = User.objects.create_user(username=username, password=password)
    user.save()

    response_data['message'] = f'Success! {username}, welcome to our website'
    return JsonResponse(response_data)


@csrf_exempt
def login_api(request):
    response_data = {}
    allowed_method = 'POST'
    if not method_check(request, allowed_method):
        response_data['message'] = 'Request method not allowed'
        return JsonResponse(response_data, status=405)
    logout(request)
    params = dict(request.POST)
    unpack(params)
    response_data = {'message': ''}

    try:
        username = params.pop('username')
        password = params.pop('password')
        if params:
            raise Exception
    except:
        response_data['message'] = 'Bad request format'
        return JsonResponse(response_data, status=400)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        response_data['message'] = f'Logged in successfully! Welcome back, {user.get_username()}'
        return JsonResponse(response_data)

    else:
        response_data['message'] = 'Incorrect username or password'
        return JsonResponse(response_data, status=401)


@csrf_exempt
def logout_api(request: HttpRequest):
    response_data = {}
    allowed_method = 'GET'
    if not method_check(request, allowed_method):
        response_data['message'] = 'Request method not allowed'
        return JsonResponse(response_data, status=405)
    logout(request)
    response_data = {'message': 'Successfully logged out!'}
    return JsonResponse(response_data)


@csrf_exempt
def status(request: HttpRequest):
    response_data = {}
    allowed_method = 'GET'
    if not method_check(request, allowed_method):
        response_data['message'] = 'Request method not allowed'
        return JsonResponse(response_data, status=405)
    response_data = {}
    ip, is_routable = get_client_ip(request)
    if request.user.is_authenticated:
        response_data['message'] = f'Logged in as {request.user.username}'
    else:
        response_data['message'] = f'Logged in as Anonymous User'

    response_data['ip'] = ip if ip is not None else 'Unknown IP'
    return JsonResponse(response_data)


@csrf_exempt
def edit(request: HttpRequest):
    response_data = {}
    allowed_method = 'POST'
    if not method_check(request, allowed_method):
        response_data['message'] = 'Request method not allowed'
        return JsonResponse(response_data, status=405)
    response_data = {'message': ''}
    if not request.user.is_authenticated:
        response_data['message'] = 'Not logged in'
        return JsonResponse(response_data, status=401)

    user = request.user
    params = dict(request.POST)
    unpack(params)
    response_data = {'message': ''}
    try:
        user_name = params.pop('username', None)
        password = params.pop('password', None)
        delete = params.pop('delete', 'False')
        if params:
            raise Exception
    except:
        response_data['message'] = 'Bad request format'
        return JsonResponse(response_data, status=400)

    if User.objects.filter(username=user_name).exists() and user_name != user.username:
        response_data['message'] = 'Failed to save chenges. Username already exists!'
        return JsonResponse(response_data)

    if user_name is not None:
        user.username = user_name
    if password is not None:
        user.set_password(password)
    user.save()
    if delete == 'True':
        user.delete()

    response_data['message'] = 'Changes saved successfully'
    return JsonResponse(response_data)


@csrf_exempt
def mobile(request: HttpRequest):
    """Return True if the request comes from a mobile device."""
    MOBILE_AGENT_RE = re.compile(
        r".*(iphone|mobile|androidtouch)", re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False


@csrf_exempt
def my_urls(request: HttpRequest):
    response_data = {}
    allowed_method = 'GET'
    if not method_check(request, allowed_method):
        response_data['message'] = 'Request method not allowed'
        return JsonResponse(response_data, status=405)
    response_data = {'message': ''}
    if not request.user.is_authenticated:
        response_data['message'] = 'Not logged in'
        return JsonResponse(response_data, status=401)

    user = request.user
    urls = Url.objects.filter(owner=user)

    url_list = {}
    for i, url in enumerate(urls):
        url_list[i+1] = dict(id=url.id, long_url=url.long_url, short_url=url.short_url,
                             desktop_clicks=url.desktop_clicks, mobile_clicks=url.mobile_clicks, clicks=url.clicks, time_created=url.time_created, last_access=url.last_access, owner=url.owner.username)

    return JsonResponse(url_list)


def unpack(dic: dict):
    for key in dic.keys():
        if isinstance(dic[key], list):
            dic[key] = dic[key][0]


def docs(request: HttpRequest):
    path = 'API/docs.html'
    return render(request, path)
