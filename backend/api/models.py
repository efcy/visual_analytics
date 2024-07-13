from django.db import models
from django.contrib.auth.models import User





class Event(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        # TODO is this function just for the admin panel?
        return self.name
