from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    # TODO
    # url(r'^list/$', event_list, name='list'),
    # url(r'^add/$', create, name='create'),
    # url(r'^(?P<slug>[\w-]+)/$', detail, name='detail'),
]
