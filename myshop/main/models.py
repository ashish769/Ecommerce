from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    title=models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.title
class Subcategory(models.Model):
    title=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title +"____" +self.category.title
class Brands(models.Model):
    title  = models.CharField(max_length=200)
    
    def _str_(self):
        return self.title
    

    
Availability_fields = (
    ('in stock', 'In Stock'),
    ('out of stock', 'Out of Stock'),
    ('pre order', 'Pre Order')
)
    

class Product(models.Model):
    image  = models.ImageField(upload_to="products", blank=True, null=True)
    image2  = models.ImageField(upload_to="products", blank=True, null=True)
    image3  = models.ImageField(upload_to="products", blank=True, null=True)
    
    name  = models.CharField(max_length=200)
    category  = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand  = models.ForeignKey(Brands, on_delete=models.CASCADE, blank=True, null=True)
    availability = models.CharField(choices=Availability_fields, max_length=200, blank=True, null=True)
    subcategory  = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    
    desc = RichTextField(blank=True)
    marked_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=4, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    
    def save(self, *args, **kwargs):
        self.price = self.marked_price * (1 - self.discount_percentage / 100)
        super().save(*args, **kwargs)
        
    def _str_(self):
        return self.name


    


    #for profile
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to="profile_picture",null=True,blank=True)
    phone_number=models.CharField(max_length=59)
    address=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.user.username

class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')#specific product ko review tannw related_NAME GARNI
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField()
    comment=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product.name