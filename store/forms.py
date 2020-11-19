from django import forms

from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('name','lastname', 'email', 'body')

    def __init__(self,user,*args,**kwargs):
        super(MessageForm, self).__init__(*args,**kwargs)
        if user.is_authenticated:
            self.fields['name'].widget = forms.HiddenInput()
            self.fields['name'].required = False
            self.fields['lastname'].widget = forms.HiddenInput()
            self.fields['lastname'].required = False
            self.fields['email'].widget = forms.HiddenInput()
            self.fields['email'].required = False

class CouponForm(forms.Form):
    code = forms.CharField()
    element_id = forms.CharField(widget=forms.HiddenInput())
