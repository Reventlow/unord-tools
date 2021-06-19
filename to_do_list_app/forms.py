from django import forms
from .models import Jobs
from django.contrib.auth.models import User

class ListForm(forms.ModelForm):
    job_owner = forms.ModelChoiceField(queryset=User.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))


    class Meta:
        model = Jobs
        fields=["item", "job_owner", "completed"]