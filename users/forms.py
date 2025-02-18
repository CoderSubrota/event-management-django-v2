from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from users.models import CustomUser
from events.models import Add_Event_Model
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password1', 'password2', 'email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class CustomRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control ring-2 ring-cyan-500 rounded my-2 ps-2 py-2 w-full flex flex-row', 'placeholder': 'Enter password'}),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control ring-2 ring-cyan-500 rounded my-2 ps-2 py-2 w-full flex flex-row', 'placeholder': 'Enter confirm password'}),
        label='Confirm Password'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name',
                  'password1', 'confirm_password', 'email', 'phone_number', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control ring-2 ring-cyan-500 rounded my-2 ps-2 py-2 w-full flex flex-row', 'placeholder': 'Enter Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control ring-2 ring-cyan-500 rounded my-2 ps-2 py-2 w-full flex flex-row', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control ring-2 ring-cyan-500 rounded my-2 ps-2 py-2 w-full flex flex-row', 'placeholder': 'Enter Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control ring-2 ring-cyan-500 rounded my-2 ps-2 py-2 w-full flex flex-row', 'placeholder': 'Enter Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control ring-2 ring-cyan-500 rounded my-2 ps-2 py-2 w-full flex flex-row', 'placeholder': 'Enter Phone Number'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control ring-2 ring-cyan-500 rounded my-2 ps-2 py-2 w-full flex flex-row'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = CustomUser.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append('Password must be at least 8 characters long')

        if not re.search(r'[A-Z]', password1):
            errors.append('Password must include at least one uppercase letter.')

        if not re.search(r'[a-z]', password1):
            errors.append('Password must include at least one lowercase letter.')

        if not re.search(r'[0-9]', password1):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$%^&+=]', password1):
            errors.append('Password must include at least one special character.')

        if errors:
            raise forms.ValidationError(errors)

        return password1

    def clean(self):  # non-field error
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'class': 'form-control w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-500 my-3',
            'placeholder': 'Enter Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-500 my-3',
            'placeholder': 'Enter Password'
        })

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role",
        widget=forms.Select(attrs={
            'class': 'block w-full px-4 py-2 mt-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    
class CreateGroupForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control border text-white my-2 border-gray-300 my-3 rounded-md p-2 w-full ring-2 ring-cyan-500 focus:border-none',
            'placeholder': 'Enter group name'
        })
    )
    
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permissions'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']



class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border text-white my-2 border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-300 focus:outline-none',
            'placeholder': 'Current Password'
        })
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border text-white my-2 border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-300 focus:outline-none',
            'placeholder': 'New Password'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border text-white my-2 border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-300 focus:outline-none',
            'placeholder': 'Confirm New Password'
        })
    )

    class Meta:
        model = forms.Form
        fields = ['old_password', 'new_password1', 'new_password2']



class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-300 focus:outline-none',
            'placeholder': 'Enter your email address'
        })
    )

    class Meta:
        fields = ['email']


class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-300 focus:outline-none',
            'placeholder': 'Enter new password'
        })
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-300 focus:outline-none',
            'placeholder': 'Confirm new password'
        })
    )

    class Meta:
        fields = ['new_password1', 'new_password2']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'profile_image']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'flex w-full p-2 border text-white my-2 border-gray-300 ring-2 ring-blue-500 text-white my-3 rounded-md focus:outline-none focus:ring-4',
                'placeholder': 'Enter your email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'flex w-full p-2 border text-white my-2 border-gray-300 ring-2 ring-blue-500 text-white my-3 rounded-md focus:outline-none focus:ring-4',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'flex w-full p-2 border text-white my-2 border-gray-300 ring-2 ring-blue-500 text-white my-3 rounded-md focus:outline-none focus:ring-4',
                'placeholder': 'Enter your last name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'flex w-full p-2 border text-white my-2 border-gray-300 ring-2 ring-blue-500 text-white my-3 rounded-md focus:outline-none focus:ring-4',
                'placeholder': 'Enter your phone number'
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'flex w-full border text-white my-2 border-gray-300 ring-2 ring-blue-500 text-white my-3 rounded-md p-2 cursor-pointer',
            }),
        }

class AddParticipantForm(UserCreationForm):
    event = forms.ModelChoiceField(
        queryset=Add_Event_Model.objects.all(),
        required=True,
        empty_label="Select an Event",
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'})
    )

    class Meta:
        model = CustomUser
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