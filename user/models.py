from django.db import models
from django.contrib.auth.models import AbstractUser

ADMIN = "Admin"
USER = "User"

class User(AbstractUser):
    role_list = (
        (ADMIN, 'Admin'),
        (USER, 'User')
    )
    
    email = models.EmailField(max_length=255, unique=True)  # Set max_length to 255 and make email unique
    username = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=100, choices=role_list, default=USER)
    text_password = models.CharField(max_length=100, blank=True, null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.email
