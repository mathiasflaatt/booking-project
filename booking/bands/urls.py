from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^add/$', add, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', detail, name='detail'),
    # TODO
    # url(r'^(?P<slug>[\w-]+)/edit/$', update, name='update'),
    # url(r'^(?P<slug>[\w-]+)/delete/$', delete, name='delete'),
]
