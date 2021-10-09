from django.conf import settings
from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from user.models import CustomerUser
from book.models import Book

class OrderItem(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete= models.CASCADE)
    item = models.ForeignKey(Book,on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price
    
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

class Order(models.Model):

    PAYMENT_METHOD = (
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Paypal', 'Paypal')
    )
    user = models.ForeignKey(CustomerUser, on_delete= models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    created_at = models.DateTimeField(auto_now_add= True)
    ordered_date = models.DateTimeField(auto_now= True)
    ordered = models.BooleanField(default=False)
    paymentId = models.CharField(max_length=255, blank=  True, null=True)
    orderId = models.CharField(max_length=255,blank=True, null= True)
    payment_method =  models.CharField(max_length=30, choices=PAYMENT_METHOD, default='Cash on Delivery')

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total



class Address(models.Model):
    user = models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank= True, null= True)
    last_name = models.CharField(max_length=20, blank= True, null= True)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True,null=True)

    def __str__(self):
        return f"{self.user.username}'s billing address"

    def is_fully_filled(self):
        field_names = {f.name for f in self._meta.get_field()}
        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True