from django.forms import ModelForm, Textarea

from .models import Comment, TypeContact

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text' : Textarea(attrs={'class':'form-input'})
        }
    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class':'form-input'})'''
    def save(self,commit=True, text=""):
        instance = super(CommentForm, self).save(commit=commit)

        if(text != ""):
            instance.text= text#"No podrás modificarme"

        if(commit):
            instance.save()
        
        return instance

from django import forms
from django.core.validators import MinLengthValidator,EmailValidator

class ContactForm(forms.Form):

    SEX = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    )

    #name = forms.CharField(label="Nombre", initial='Pepe', required=True, disabled=False, help_text='Aquí va tu nombre y no el de tu tía', max_length=10, min_length=3)    
    name = forms.CharField(label="Nombre", max_length=10, min_length=3 ) #validators=[MinLengthValidator(2, message='Muy corto! (minino %(limit_value)d) actual %(show_value)d ')]   widget=forms.(attrs={'class':'form-control'})
    #email = forms.CharField(label='Correo', validators=[EmailValidator(message='Correo inválido', whitelist=['gmail'])])
    email = forms.EmailField(label='Correo', initial='andres@gmail.com')
    surname = forms.CharField(label="Apellido", required=False, max_length=10, min_length=3)    
    phone = forms.RegexField(label='Teléfono',regex='\(\w{3}\)\w{3}-\w{4}', max_length=13, min_length=13, initial='(123)123-1234')
    date_birth = forms.DateField(label='Fecha de nacimiento',initial='1990-11-29')
    #type_contact = forms.ChoiceField(label='Tipo de contacto', choices=CHOICE, initial=20)
    type_contact = forms.ModelChoiceField(label='Tipo de contacto', queryset=TypeContact.objects.all(), initial=2)
    sex = forms.ChoiceField(label='Sexo', choices=SEX)
    document = forms.FileField(label='Documento', required=False)
    tems = forms.BooleanField(label='Condiciones de servicio')
    
    