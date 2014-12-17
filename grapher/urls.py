from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^(?P<stream_name>.*)$', views.show_graph),
)
