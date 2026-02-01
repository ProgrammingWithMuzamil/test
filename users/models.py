from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username']  

    def __str__(self):
        return self.email


class Property(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    img = models.ImageField(upload_to='properties/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Collaboration(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    img = models.ImageField(upload_to='collaborations/', null=True, blank=True) 
    logo = models.ImageField(upload_to='collaborations/logos/', null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Slide(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    img = models.ImageField(upload_to='slides/', null=True, blank=True)  
    points = models.JSONField(default=list)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class YourPerfect(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    img = models.ImageField(upload_to='yourperfect/', null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class SidebarCard(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField() 
    img = models.ImageField(upload_to='sidebarcard/', null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Damac(models.Model):
    video = models.URLField()  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Video {self.id}"
    


class EmpoweringCommunities(models.Model):
    video = models.URLField()  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"Empowering Community Video {self.id}"