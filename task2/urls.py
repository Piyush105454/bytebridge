from django.urls import path
from . import views

urlpatterns = [
    path('Signup/', views.Signup, name='Signup'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]
