from django.contrib import admin
from django.urls import path
from .views import check_in, check_out, register, login_view, user_logout

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),
    path('check-in/<str:email>/', check_in, name='check_in'),
    path('check-out/<str:email>/', check_out, name='check_out'),
]
