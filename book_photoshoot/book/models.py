from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField()
    city = models.CharField(max_length=15)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.user
