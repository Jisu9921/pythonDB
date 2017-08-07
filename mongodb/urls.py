import django.conf.urls

from .views import mongo_index

urlpatterns = [
    django.conf.urls.url(r'^$', mongo_index, name='mongo_index'),
]
