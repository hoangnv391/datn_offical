from . import models
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = models.users
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(),
        }

