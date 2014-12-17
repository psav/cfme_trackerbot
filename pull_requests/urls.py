from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^pr/(?P<pr_number>\d+)$', views.pr_detail),
    url(r'^run/(?P<run_number>\d+)$', views.run_detail),
    url(r'^retest/(?P<pr_number>\d+)$', views.retest),
)
