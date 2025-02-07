from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group,Permission
from django import forms 
from events.models import Add_Event_Model
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
         
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400',
                'placeholder': field.label
            })
            
class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role",
        widget=forms.Select(attrs={
            "class": "w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        })
    )
    
class CreateGroupForm(forms.ModelForm):
    permission = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        label="Assign Permission",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "space-y-2 my-3"})
    )

    class Meta:
        model = Group
        fields = ["name", "permission"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "w-full p-2 border rounded-md", "placeholder": "Enter group name"}),
        }

class Add_Participant(UserCreationForm):
    event = forms.ModelChoiceField(
        queryset=Add_Event_Model.objects.all(),
        required=True,
        empty_label="Select an Event",
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'event']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400',
                'placeholder': field.label
            })
