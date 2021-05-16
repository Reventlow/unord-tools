from django import forms
from .models import Jobs

class ListForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields=["item", "completed"]