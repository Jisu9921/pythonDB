import django.conf.urls

from .views import *

urlpatterns = [
    django.conf.urls.url(r'^$', scheduler_index, name='scheduler_index'),
    django.conf.urls.url(r'^insert/$', insert_schedule, name='insert'),
    django.conf.urls.url(r'^get/$', get_schedule, name='get'),
    django.conf.urls.url(r'^delete/$', delete_schedule, name='delete'),
]
