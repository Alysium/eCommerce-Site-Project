from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    postal_code = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, \
    	help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'postal_code',\
        	'first_name', 'last_name', 'email',\
        	'password1', 'password2', )
