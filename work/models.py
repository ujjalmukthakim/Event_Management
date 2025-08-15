
from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField(null=True)
    
    def __str__(self):
        return self.name


class Event(models.Model):


    name=models.CharField(max_length=50)
    description=models.TextField(null=True)
    create_date = models.DateField(auto_now_add=True)
    start_date=models.DateField(auto_now=False, auto_now_add=False)
    time=models.TimeField()
    location=models.TextField(max_length=50)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="reverse_category")
    participant=models.ManyToManyField(User,related_name="reverse_user")
    rsvps = models.ManyToManyField(User, related_name="rsvp_events", blank=True)
    pic = models.ImageField(upload_to='', blank=True, null=True,default='default.jpg')


    def __str__(self):
        return self.name

    









