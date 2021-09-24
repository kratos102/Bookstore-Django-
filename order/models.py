from django.db import models
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
    user = models.ForeignKey(CustomerUser, on_delete= models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    created_at = models.DateTimeField(auto_now_add= True)
    ordered_date = models.DateTimeField(auto_now= True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total