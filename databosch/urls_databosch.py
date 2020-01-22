from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from django.contrib.auth.models import Group
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

admin.site.site_title = 'DataBosch 2.0'
admin.site.site_header = 'DataBosch 2.0'
admin.site.site_url = None
admin.site.index_title = 'Overzicht'
