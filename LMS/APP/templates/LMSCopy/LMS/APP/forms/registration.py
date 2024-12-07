from django import forms
from ..models import User
class Registration(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm_password",widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password doesnt match')
        return cd['password2']
    