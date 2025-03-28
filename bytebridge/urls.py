from django.urls import path
from task2 import views

urlpatterns = [
    path('', views.register, name='register'),  # Home page & Registration
]
