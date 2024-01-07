from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type":"date"}))

    class Meta:
        model = Task
        exclude = ['user', 'done']