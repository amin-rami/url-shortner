import json
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
import json


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


    return HttpResponse('Success!')


def redirect_api(requset: HttpRequest):
    pass