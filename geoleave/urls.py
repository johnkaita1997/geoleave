from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from geoleave import settings

api_version = 'api/v1/'

api_patterns = [
    path(api_version + 'users/', include('appuser.urls')),
    path(api_version + 'files/', include('file_upload.urls')),
    path(api_version + 'web/', include('web.urls')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('', include('web.urls')),

]

urlpatterns = api_patterns + [
    path('admin/', admin.site.urls),
]


