from django.conf import settings


def inject_urls(request):
    return {
        'base_url': settings.BASE_URL,
        'jenkins_url': settings.JENKINS_URL
    }
