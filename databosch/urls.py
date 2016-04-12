from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import Group

urlpatterns = [
    url(r'', admin.site.urls),
]

admin.site.site_title = 'DataBosch'
admin.site.site_header = 'DataBosch'
admin.site.site_url = None
admin.site.index_title = 'Overzicht'
admin.site.unregister(Group)
