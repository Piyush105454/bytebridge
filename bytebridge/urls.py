from django.urls import path
from task2 import views
from django.urls import path, include


urlpatterns = [
   
     path('', include('task2.urls')),  # Make sure this line is present
   
]
