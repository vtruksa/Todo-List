from django import forms
from django.contrib.auth.models import User

from .models import Task

class TaskForm(forms.ModelForm):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type":"date"}))

    class Meta:
        model = Task
        exclude = ['user', 'done']

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
