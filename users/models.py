from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profile_images', blank=True, default='profile_images/default.jpg')
    phone_number = models.TextField(blank=True)
    event_assign = models.ManyToManyField("events.Add_Event_Model", related_name="participants")

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

    def __str__(self):
        return self.username
