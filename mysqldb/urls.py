import django.conf.urls

from .views import mysql_index

urlpatterns = [
    django.conf.urls.url(r'^$', mysql_index, name='mysql_index'),
]
