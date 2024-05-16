from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class User(models.Model):
#     first_name = models.CharField(max_length=128)
#     last_name = models.CharField(max_length=128)
#     email_field = models.EmailField(max_length=254, unique=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #default: on_delete=models.CASCADE
    # portfolio_site = models.URLField(blank=True) 
    # profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    def __str__(self):
        return self.user.username