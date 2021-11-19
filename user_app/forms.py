from django import forms
from user_app import models


class LoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('username','password')
        # fields = '__all__'