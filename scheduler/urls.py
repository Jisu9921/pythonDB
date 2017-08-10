import django.conf.urls

from .views import *

urlpatterns = [
    django.conf.urls.url(r'^$', scheduler_index, name='scheduler_index'),
]
