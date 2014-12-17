from django.conf.urls import patterns, url
import views

# Note that these views are included at the root URL (/), not in a dashboard namespace
urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^retest$', views.retest),
    url(r'^sauce_proxy/(?P<sauce_url>.*)$', views.sauce_proxy),
)
