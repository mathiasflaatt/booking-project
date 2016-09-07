from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    # TODO
    url(r'^events/$', list, name='list'),
    url(r'^events/add/$', add, name='create'),
    url(r'^events/(?P<slug>[\w-]+)/$', detail, name='detail'),
]
