from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .views import home
from . import settings
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('',home, name='home'),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('administrator/', include('administration.urls')),
    path('voting/', include('voting.urls')),
    path('api/', include('api.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

