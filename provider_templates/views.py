import random

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from models import ProviderTemplateDetail


def templates_to_test(request):
    # This is a silly view for the jenkins URL polling plugin
    # The plugin works by triggering a build if the contents of a URL have changed
    # since the last poll. So we'll generate a random string if the number of
    # untested templates is more than 0, and just return nothing if it is 0.
    if ProviderTemplateDetail.objects.filter(tested=False):
        text = ''.join([chr(random.randint(48, 122)) for i in range(32)])
    else:
        text = ''

    return HttpResponse(text, content_type="text/plain")


def retest(request, provider_key, template_name):
    ptd = get_object_or_404(ProviderTemplateDetail, provider=provider_key, template=template_name)
    ptd.tested = False
    ptd.save()
    msg = 'Template "{}" on provider "{}" marked for retest'.format(template_name, provider_key)
    return HttpResponse(msg, content_type="text/plain")
