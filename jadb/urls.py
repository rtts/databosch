from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^$', Entities.as_view()),
]
