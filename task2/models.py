from django.db import models
from django.contrib.auth.hashers import make_password

class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, default=make_password("defaultpassword"))  # Temporary default password
    checked_in = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
