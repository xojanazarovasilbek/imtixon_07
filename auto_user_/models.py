from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Address(models.Model):
    name = models.CharField(max_length=150)


    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(max_length=225, blank=True, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.username
    



