from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import requests
import json


def sauce_proxy(request, sauce_url):
    params = []
    for param in request.REQUEST:
        params.append("{}={}".format(param, request.REQUEST[param]))
    param_string = "&".join(params)
    if not sauce_url.startswith('rest/v1/$user$/jobs'):
        return
    sauce_url = sauce_url.replace('$user$', settings.SAUCE_USER)
    r = requests.get('https://saucelabs.com/{}?{}'.format(sauce_url, param_string),
                     auth=(settings.SAUCE_USER, settings.SAUCE_API))
    jdata = json.dumps(r.json())
    if 'callback' in request.REQUEST:
        data = '{}({});'.format(request.REQUEST['callback'], jdata)
    else:
        data = jdata
    return HttpResponse(data, "application/json")


def home(request):
    return render(request, 'home.html')


def retest(request):
    return render(request, 'retest.html')
