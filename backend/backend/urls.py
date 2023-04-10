from django.contrib import admin
from django.urls import path, include

from .yasg import urlpatterns as docs_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += docs_urls
