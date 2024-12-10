from django import forms
from django.contrib.auth.models import User

class SellerRegistration(forms.ModelForm):
    password=forms.CharField(label='Password', widget=forms.PasswordInput)
    cpassword=forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    email=forms.EmailField(required=True)
    phone=forms.IntegerField(label='Phone',widget=forms.TextInput(attrs={'placeholder':'enter your phone number'}))
    class Meta:
        model = User
        fields=['username','first_name','last_name','email','phone','password','cpassword']