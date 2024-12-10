from django.db import models
from django.db.models import Q
from django.urls import reverse
# Create your models here.
class Seller(models.Model):
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
class House(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='pictures/')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE,default=1) ## NEW


    def __str__(self):
        return self.title
    
    def get_comments(self):
        # Retrieve all comments associated with this house
        return self.comments.all() 
    
class Buyer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    photo = models.ImageField(upload_to='photoes/')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

    
class Comment(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="comments")
    author_name = models.CharField(max_length=100)  # For anonymous or non-registered users
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author_name} on {self.house.title}"
    
