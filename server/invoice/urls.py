from django.urls import path
from . import views

app_name = 'invoice'  # or 'invoice' for invoice/urls.py
urlpatterns = [
    # Add your URL patterns here
    path('debug-media/<path:path>', views.debug_media, name='debug_media'),
]