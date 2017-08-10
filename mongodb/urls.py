import django.conf.urls
from .views import *

urlpatterns = [
    django.conf.urls.url(r'^insert_schedule/$', insert_schedule_mongo, name='insert_schedule'),
    django.conf.urls.url(r'^get_schedule/$', get_schedule_mongo, name='get_schedule'),
    django.conf.urls.url(r'^delete_schedule/$', delete_schedule_mongo, name='delete_schedule'),
]
