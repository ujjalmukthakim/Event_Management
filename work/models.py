from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    participant = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="events_participated")
    rsvps = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="rsvp_events", blank=True)
    pic = models.ImageField(upload_to='event_pics/', blank=True, null=True, default='default.jpg')

    def __str__(self):
        return self.name
    
