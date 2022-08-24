from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest


def shortner_api(request: HttpRequest):
    params = dict(request.GET)
    try:
        long_url = params.pop('url')
        if params:
            raise Exception
    except:
        return HttpResponseBadRequest('Bad Request')

        
    return HttpResponse('Success!')


def redirect_api(requset: HttpRequest):
    pass