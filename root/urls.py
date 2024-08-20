from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from root.settings import MEDIA_URL, MEDIA_ROOT, STATIC_URL, STATIC_ROOT

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("ckeditor5/", include('django_ckeditor_5.urls')),
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  path('api/', include('apps.urls')),
                  path('', include('rest_framework.urls')),
                  path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
              ] + static(MEDIA_URL, document_root=MEDIA_ROOT) + static(STATIC_URL, document_root=STATIC_ROOT)
