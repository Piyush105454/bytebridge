from django.urls import path
from .views import check_in, check_out, register

urlpatterns = [
    path('check-in/<str:email>/', check_in, name='check_in'),
    path('check-out/<str:email>/', check_out, name='check_out'),
     path('', register, name='register'),
]
