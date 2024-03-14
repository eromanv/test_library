# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


class Organization(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)
    members = models.ManyToManyField(CustomUser, related_name='organizations')
    
    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    organizations = models.ManyToManyField(Organization, related_name="events")
    image = models.ImageField(upload_to="event_images/", null=True, blank=True)
    date = models.DateField()

    def get_users(self):
        users = set()
        for organization in self.organizations.all():
            users.update(organization.members.all())
        return users

    def __str__(self):
        return self.title
