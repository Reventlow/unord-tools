from django import forms
from .models import Jobs
from django.contrib.auth.models import User

class ListForm(forms.ModelForm):

    class Meta:
        model = Jobs
        fields=["item", "job_owner", "completed"]