from django.db import models
from django.contrib.auth import get_user_model
from event_management import settings
CustomUser = get_user_model()
# Create your models here.
class Category_Model(models.Model):
    name = models.CharField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Add_Event_Model(models.Model):
    name = models.TextField()
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.TextField()
    image = models.ImageField(max_length=5200,upload_to='event_images/', default='event_images/default.png')
   
    category = models.ForeignKey(
    Category_Model,  
    related_name="categories",
    on_delete=models.CASCADE
)

    def __str__(self):
        return self.name


class Create_Participant_Model(models.Model):
    name = models.TextField()
    email = models.EmailField(unique=True) 
    event_assign = models.ManyToManyField(Add_Event_Model, related_name="events")

    def __str__(self):
        return self.name


class RSVP_Model(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Add_Event_Model, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')
        
