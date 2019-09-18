from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.views import static

from . import views


app_name = 'xremote'
urlpatterns = [
    path('', views.DownloadRemote.as_view(), name='download')
]

if settings.DEBUG:
    urlpatterns += [
        path('media/<path:path>', static.serve, kwargs={'document_root': settings.MEDIA_ROOT})
    ]
