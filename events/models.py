from django.db import models

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
    image = models.ImageField(upload_to='event_images/', default='default_event.jpg')
   
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

