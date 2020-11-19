
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from django.utils.translation import gettext as _

from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email', 
    max_length=50,
    help_text=_('Put your favorite email'),
    error_messages={'invalid':"Solamente puedes colocar caracteres válidos para un email"})

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        u = User.objects.filter(email = email)
        if u.count():
            raise ValidationError(_("Email taking"))
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar','user')
        
    def __init__(self,*args,**kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].required = False
        self.fields['avatar'].widget.attrs['class'] = "custom-file-input"
        self.fields['avatar'].widget.attrs['id'] = "customFile"
    
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        w, h = get_image_dimensions(avatar)

        print(len(avatar))

        #validacion por tamano de la img
        max_width = max_height = 600
        if w > max_width or h > max_height:
            raise forms.ValidationError("Imagen muy grande, la imagen no puede superar las %spx, %spx" % (max_width, max_height))
        
        # extension
        m,t = avatar.content_type.split('/')
        if not(m == 'image' and t in ['jpeg', 'jpg', 'gif', 'png']):
            raise forms.ValidationError("Imagen no soportada, solamente soportamos: 'jpeg', 'jpg', 'gif', 'png'")
        
        #tamano de la imagen 1 KB equivale a 1024B
        if len(avatar) > (30 * 1024):
            raise forms.ValidationError("Imagen no puede superar los 30kb")

        return avatar
