import django.conf.urls

from .views import dynamo_index

urlpatterns = [
    django.conf.urls.url(r'^$', dynamo_index, name='dynamo_index'),
]
