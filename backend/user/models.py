from django.db import models

from django.contrib.auth.models import AbstractUser

class vat_user(AbstractUser):
    name = models.CharField(max_length=100)
    first_name = models.Charfield(max_length=100)
    email = models.EmailField(max_length=254)
    token = models.CharField(max_length=100)
