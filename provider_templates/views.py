import random

from django.http import HttpResponse

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


def retest(request, provider_key=None, template_name=None):
    if provider_key and template_name:
        filter = {'provider': provider_key, 'template': template_name}
        msg = 'Template "{}" marked for retest on provider "{}"'.format(template_name, provider_key)
    elif provider_key:
        filter = {'provider': provider_key}
        msg = 'All templates marked for retest on provider "{}"'.format(provider_key)
    elif template_name:
        filter = {'template': template_name}
        msg = 'Template "{}" marked for retest on all providers'.format(template_name)

    updated = ProviderTemplateDetail.objects.filter(**filter).update(tested=False)

    if not updated:
        msg = "No templates marked for retest (no matches)."

    return HttpResponse(msg, content_type="text/plain")


def mark(request, mark, provider_key=None, template_name=None):
    # mark should only be usable or unusable
    if mark == 'usable':
        usable = True
    else:
        usable = False

    if provider_key and template_name:
        filter = {'provider': provider_key, 'template': template_name}
        msg = 'Template "{}" marked {} on provider "{}"'.format(template_name, mark, provider_key)
    elif provider_key:
        filter = {'provider': provider_key}
        msg = 'All templates marked {} on provider "{}"'.format(mark, provider_key)
    elif template_name:
        filter = {'template': template_name}
        msg = 'Template "{}" marked {} on all providers'.format(template_name, mark)

    updated = ProviderTemplateDetail.objects.filter(**filter).update(usable=usable)

    if not updated:
        msg = "No templates marked {} (no matches).".format(mark)

    return HttpResponse(msg, content_type="text/plain")
