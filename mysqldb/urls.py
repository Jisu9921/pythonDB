import django.conf.urls

from .views import *

urlpatterns = [
    django.conf.urls.url(r'^$', mysql_index, name='mysql_index'),
    django.conf.urls.url(r'^insert_schedule/$', insert_schedule_mysql, name='insert_schedule'),
    django.conf.urls.url(r'^get_schedule/$', get_schedule_mysql, name='get_schedule'),
    django.conf.urls.url(r'^delete_schedule/$', delete_schedule_mysql, name='delete_schedule'),
]
