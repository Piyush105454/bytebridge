from django.urls import path
from task2 import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   
     path('', include('task2.urls')),  # Make sure this line is present
   
]

# Serve static and media files correctly in production
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
