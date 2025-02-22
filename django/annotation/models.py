
from django.db import models
from image.models import NaoImage


class Annotation(models.Model):
    image= models.OneToOneField(NaoImage,on_delete=models.CASCADE,related_name='Annotation', primary_key=True)
    annotation = models.JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
