from django.db import models
from django.shortcuts import reverse 

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, default='')
    def __str__(self) -> str:
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255, default='')
    def __str__(self) -> str:
        return self.name

class Author(models.Model):
    name = models.CharField(max_length= 255, default='')
    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    title = models.CharField(max_length= 255, default='')
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    author = models.ForeignKey(Author, on_delete= models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete= models.CASCADE)
    description = models.TextField(default='This is a book')
    price = models.IntegerField(default=0)
    discount_price = models.IntegerField(blank=True, null= True)
    slug = models.SlugField()
    quantity = models.IntegerField(default=0)
    active = models.BooleanField(default= True)
    image = models.ImageField(null= True, blank = True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("product", kwargs={
            "slug": self.slug
        })

    @property
    def imageURL(self):
        try :
            url =self.image.url
        except:
            url = ''
        return url   

    def get_add_to_shoppingcart_url(self):
        return reverse("add-to-shoppingcart", kwargs={
        'slug': self.slug
    })  

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
        'slug': self.slug
    })  