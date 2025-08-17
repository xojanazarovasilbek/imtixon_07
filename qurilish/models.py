from django.db import models
from auto_user_.models import CustomUser
# from django.contrib.auth.models import User 
# Create your models here.
from django.utils import timezone



class Categroy(models.Model):
    name = models.CharField(max_length=120)



class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Categroy, on_delete=models.CASCADE, related_name='category')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    desc = models.TextField()
    image = models.ImageField(upload_to="media/",blank=True, null=True)
    create_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.user},{self.category}"





class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")  
    text = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)     

    def __str__(self):
        return f"{self.user.username} - {self.text[:20]}"