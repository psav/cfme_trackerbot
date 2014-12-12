from django.http import HttpResponse
import requests
import json
from settings import SAUCE_API, SAUCE_USER


def sauce_proxy(request, sauce_url):
    params = []
    for param in request.REQUEST:
        params.append("{}={}".format(param, request.REQUEST[param]))
    param_string = "&".join(params)
    if not sauce_url.startswith('rest/v1/$user$/jobs'):
        return
    sauce_url = sauce_url.replace('$user$', SAUCE_USER)
    r = requests.get('https://saucelabs.com/{}?{}'.format(sauce_url, param_string),
                     auth=(SAUCE_USER, SAUCE_API))
    jdata = json.dumps(r.json())
    if 'callback' in request.REQUEST:
        data = '{}({});'.format(request.REQUEST['callback'], jdata)
    else:
        data = jdata
    return HttpResponse(data, "application/json")
