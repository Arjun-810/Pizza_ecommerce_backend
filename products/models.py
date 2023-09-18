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
    ingredients = models.ManyToManyField(Ingredients)
    item_name = models.CharField(max_length=100)
    soldOut = models.BooleanField(default=False)
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, null=False, default="INSERT")

    def __str__(self):
        return self.item_name
    


class User(AbstractUser):
    contact_number = models.CharField(max_length=15)
    name = models.CharField(max_length=150, null=True, blank=False)
    is_active = models.IntegerField(default=1)
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text="Optional. Usernames must be unique.",
    )
    def __str__(self):
        return self.name

class ProductCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name="user_cart")
    item_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE,null=True, related_name="product_cart")
    quantity = models.PositiveIntegerField(null=False)

    def __str__(self):
        return self.user_id.name + " " + self.item_id.item_name
    

class Order(models.Model):
    total_amount =  models.PositiveIntegerField(null=False)
    contact_no = models.CharField(max_length=15, null= False)
    client_name = models.CharField(max_length=50, null=False, blank=False)
    delivery_address = models.CharField(max_length=150, null=False, blank=False)
    order_status = models.CharField(max_length=15, null=False, default="PENDING")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True, related_name="user_order")
    stripe_session_id = models.CharField(max_length=150, null=True, blank=False)
    def __str__(self):
        return self.user_id.name + " " + self.order_status
    
class OrderItem(models.Model):
    item_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE,null=True, related_name="product_order")
    quantity = models.PositiveIntegerField(null=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE,null=True, related_name="order_map")


    def __str__(self):
        return self.order_id.client_name + " " + self.item_id.item_name