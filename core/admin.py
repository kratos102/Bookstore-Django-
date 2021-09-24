from django.contrib import admin
from book.models import Book, Category, Author, Publisher
from order.models import Order, OrderItem
from user.models import CustomerUser


admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CustomerUser)