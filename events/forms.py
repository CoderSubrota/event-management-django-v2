
from django import forms
from events.models import Create_Participant_Model,Category_Model,Add_Event_Model

class Add_Event (forms.ModelForm):
    class Meta:
        model = Add_Event_Model
        fields = ['name','description','date','time','location','category','image']
        
        widgets={
            'name':forms.TextInput(attrs={
                'class':'py-3 ps-2 rounded-xl flex w-full my-4 flex-col ring-2 ring-indigo-500',
                'placeholder':'Enter participant name'
            }),
            'description':forms.TextInput(attrs={
                'class':'py-3 ps-2 rounded-xl flex w-full my-4 flex-col ring-2 ring-indigo-500',
                'placeholder':'Enter participant description'
            }),
            'date':forms.DateInput(attrs={
                'type':'date',
                'class':'py-3 ps-2 rounded-xl flex w-full my-4 flex-col ring-2 ring-indigo-500',
            }),
            'time':forms.TimeInput(attrs={
                 'type':'time',
                 'class':'py-3 ps-2 rounded-xl flex w-full my-4 flex-col ring-2 ring-indigo-500',
                 'placeholder':'Follow this formate HH:MM:SS'
            }),
            'location':forms.TextInput(attrs={
                'class':'py-3 ps-2 rounded-xl flex w-full my-4 flex-col ring-2 ring-indigo-500',
                
                'placeholder':'Enter participant location'
            }),
              'image':forms.FileInput(attrs={
                  'class':'py-3 ps-2 rounded-xl flex w-full my-4 flex-col ring-2 ring-indigo-500 mt-3',
            })
        
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        

class Add_Category (forms.ModelForm):
    class Meta:
        model = Category_Model
        fields = ['name','description']
        
        widgets={
            'name':forms.TextInput(attrs={
                'class':'py-3 ps-2 rounded-xl flex w-full my-4 flex-col ring-2 ring-indigo-500',
                'placeholder':'Enter category name'
            }),
            'description':forms.Textarea(attrs={
                'class':'py-3 ps-2 rounded-xl flex w-full my-4 h-56 flex-col ring-2 ring-indigo-500',
                'placeholder':'Enter category description'
            }),
        }
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args,**kwargs)
            
class Create_Participant_Form(forms.ModelForm):
    class Meta:
        model = Create_Participant_Model
        fields = ['name', 'email', 'event_assign']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'py-3 px-4 rounded-xl w-full my-4 border border-indigo-500 focus:ring-4 focus:ring-indigo-700',
                'placeholder': 'Enter participant name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'py-3 px-4 rounded-xl w-full my-4 border border-indigo-500 focus:ring-4 focus:ring-indigo-700',
                'placeholder': 'Enter participant email'
            }),
            'event_assign': forms.CheckboxSelectMultiple(attrs={
                'class': 'flex flex-col space-y-2 my-4'
            })
        }
