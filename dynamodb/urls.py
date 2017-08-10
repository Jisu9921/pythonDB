import django.conf.urls
from .views import *

urlpatterns = [
    django.conf.urls.url(r'^create_table/$', create_table_dynamon, name='create_table'),
    django.conf.urls.url(r'^insert_schedule/$', insert_schedule_dynamo, name='insert_schedule'),
    django.conf.urls.url(r'^get_schedule/$', get_schedule_dynamo, name='get_schedule'),
    django.conf.urls.url(r'^delete_schedule/$', delete_schedule_dynamo, name='delete_schedule'),
]
