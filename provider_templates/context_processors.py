from django.conf import settings


def bootstrap_version(request):
    return {'bootstrap_version': settings.BOOTSTRAP_VERSION}
