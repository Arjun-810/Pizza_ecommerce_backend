from django.db import models
from django.contrib.auth.models import AbstractUser


class Ingredients(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingedrient_name = models.CharField(max_length=150, null=False, blank=False)
    status = models.CharField(max_length=15, null=False, default="INSERT")

    def __str__(self):
        return self.ingedrient_name

class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    imageUrl = models.URLField()
    ingredients = models.ManyToManyField(Ingredients,null=True)
    item_name = models.CharField(max_length=100)
    soldOut = models.BooleanField(default=False)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, null=False, default="INSERT")

    def __str__(self):
        return self.item_name
    


class User(AbstractUser):
    contact_number = models.CharField(max_length=15)
    name = models.CharField(max_length=150, null=True, blank=False)
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text="Optional. Usernames must be unique.",
    )