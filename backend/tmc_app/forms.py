from django import forms
# import the particular table from models
from .models import Users
class UserForm(forms.ModelForm):
    class Meta:
        model = Users #table name
        fields = [
            'username',
            'psw',
            'email'
        ]