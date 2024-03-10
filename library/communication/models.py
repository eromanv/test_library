# myapp/models.py
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Organization(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    organizations = models.ManyToManyField(Organization, related_name="events")
    image = models.ImageField(upload_to="event_images/", null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        return self.title
