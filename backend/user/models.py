from django.db import models

from django.contrib.auth.models import AbstractUser

class organization(models.Model):
    name = models.CharField(max_length=100)


class vat_user(AbstractUser):
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    token = models.CharField(max_length=100)
    orga = models.ForeignKey(organization,on_delete=models.CASCADE,related_name='organizations',blank=True,null=True)
    
    def __str__(self):
        return self.first_name