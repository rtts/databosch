from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import Group
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = 'DataBosch'
admin.site.site_header = 'DataBosch'
admin.site.site_url = None
admin.site.index_title = 'Overzicht'
admin.site.unregister(Group)
