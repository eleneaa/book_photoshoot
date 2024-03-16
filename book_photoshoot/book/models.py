from django.conf import settings
from django.db import models
from django.utils import timezone


class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField()
    city = models.CharField(max_length=15)
    photo_studio = models.TextField()
    people_count = models.PositiveIntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.user
