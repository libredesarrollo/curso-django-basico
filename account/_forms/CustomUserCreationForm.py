
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email', 
    max_length=50,
    help_text='Coloca tu email de preferencia.',
    error_messages={'invalid':"Solamente puedes colocar caracteres válidos para un email"})

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        u = User.objects.filter(email = email)
        if u.count():
            raise ValidationError("Email ya ha sido tomado")
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user