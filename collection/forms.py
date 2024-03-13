from django import forms
from django.forms import TextInput

class LoginForm(forms.Form):
   u_name = forms.CharField(label="User Id:", max_length = 50, widget=forms.TextInput(attrs={'class': 'form-control'}))
   u_pass = forms.CharField(label="Password:", max_length = 20, widget = forms.PasswordInput(attrs={'class': 'form-control'}))


                    