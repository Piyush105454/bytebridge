from django.contrib import admin
from .models import Registration

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'checked_in')  # Show these columns in admin
    search_fields = ('email', 'name')  # Search bar for name & email
    list_filter = ('checked_in',)  # Filter users by check-in status

admin.site.register(Registration, RegistrationAdmin)
