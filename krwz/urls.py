from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('users.urls', namespace='users')),
    path('', include('main.urls', namespace='main')),
    path('admin/', admin.site.urls),
    path('api/', include('main.api.urls', namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
