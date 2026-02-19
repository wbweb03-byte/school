from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import About  , Letter, Notice, Gallery, Logo
from django import forms
from .models import About

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']





class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['title', 'description', 'image', 'is_published']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Enter title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'rows': 5,
                'placeholder': 'Write description here'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'mr-2'
            }),
        }

class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ['name', 'subject', 'description', 'image', 'is_published']

        labels = {
            'name': 'Principal Name',
            'subject': 'Subject',
            'description': 'Description',
            'image': 'Upload Image',
            'is_published': 'Publish'
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Enter principal name'
            }),

            'subject': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Enter your subjects'
            }),

            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'rows': 10,
                'placeholder': 'Enter your description here'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full',
                'accept': 'image/*'
            }),

            'is_published': forms.CheckboxInput(attrs={
                'class': 'mr-2 align-middle'
            })
        }

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description', 'is_published']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded',
                'placeholder': 'Enter Notice title'
            }),

            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'rows': 10,
                'placeholder': 'Enter your description here'
            }),

            'is_published': forms.CheckboxInput(attrs={
                'class': 'mr-2 align-middle'
            }),
        }



class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image']
        widgets = {
        'image': forms.ClearableFileInput(attrs={
            'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none',
            'accept': 'image/*'
        })
    }
        
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageUploadForm(forms.Form):
    images = forms.ImageField(
        widget=MultiFileInput(attrs={
            'multiple': True,
            'class': 'block w-full border p-2 rounded-lg',
            'accept': 'image/*'
        })
    )




class LogoForm(forms.ModelForm):
    class Meta:
        model = Logo
        fields = ['logo', 'school_name', 'school_name_short', 'slug']
        widgets = {
            'logo': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm border rounded-lg p-2'
            }),
            'school_name': forms.TextInput(attrs={
                'class': 'w-full border rounded-lg p-2'
            }),
            'school_name_short': forms.TextInput(attrs={
                'class': 'w-full border rounded-lg p-2'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full border rounded-lg p-2'
            }),
        }
