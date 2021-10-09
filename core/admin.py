from django.contrib import admin
from book.models import *
from order.models import *
from user.models import *



admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CustomerUser)
admin.site.register(Address)