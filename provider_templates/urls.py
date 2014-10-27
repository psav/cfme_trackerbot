from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^to_test$', 'provider_templates.views.templates_to_test'),
    url(r'^retest/(?P<provider_key>.+)/(?P<template_name>.+)$',
        'provider_templates.views.retest'),
)
