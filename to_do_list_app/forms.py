from django import forms
from .models import Jobs
from django.contrib.auth.models import User

class JobsForm(forms.ModelForm):

    class Meta:
        model = Jobs
        fields=["item", "to_do_owner", "completed"]