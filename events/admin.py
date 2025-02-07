from django.contrib import admin
from events.models import Create_Participant_Model, Add_Event_Model,Category_Model
# Register your models here.
admin.site.register(Create_Participant_Model) 
admin.site.register(Add_Event_Model) 
admin.site.register(Category_Model)

 