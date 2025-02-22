from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

schema_view = get_schema_view(
   openapi.Info(
      title="Orders API",
      default_version='v1',
      description="""
      API documentation for Orders System
      
      How to use:
      1. First get your token at /auth/jwt/create/
      2. Click 'Authorize' button and enter token as: Bearer <your_token>
      3. Now you can use all API endpoints
      """,
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=(),
)

urlpatterns = [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += [
    # Admin endpoint
    path('admin/', admin.site.urls),
    # Auth endpoints
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),
    path('api/', include('orders.urls')),
    path('api/crm/', include('crm.urls')),
    path('api/invoice/', include('invoice.urls')),
    # Media serving - add this before the static pattern
    path('media/<path:path>', serve, {
        'document_root': settings.MEDIA_ROOT,
    }, name='media'),
]

# Add static and media patterns for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)