from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^to_test$', 'provider_templates.views.templates_to_test'),
    url(r'^retest/(?P<provider_key>.+)/all$',
        'provider_templates.views.retest'),
    url(r'^retest/all/(?P<template_name>.+)$',
        'provider_templates.views.retest'),
    url(r'^retest/(?P<provider_key>.+)/(?P<template_name>.+)$',
        'provider_templates.views.retest'),
    # These retest and mark views are redundant, but help make things a little easier in JS
    # this work should be done with the API, and these views should go away
    url(r'^mark/(?P<mark>unusable|usable)/(?P<provider_key>.+)/all$',
        'provider_templates.views.mark'),
    url(r'^mark/(?P<mark>unusable|usable)/all/(?P<template_name>.+)$',
        'provider_templates.views.mark'),
    url(r'^mark/(?P<mark>unusable|usable)/(?P<provider_key>.+)/(?P<template_name>.+)$',
        'provider_templates.views.mark'),
)
