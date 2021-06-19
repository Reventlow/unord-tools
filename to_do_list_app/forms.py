from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Jobs


class JobsForm(forms.ModelForm):
    item = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Opgave beskrivelse'}))
    to_do_owner = forms.CharField(widget=forms.HiddenInput(), initial={"option": User.id})
    completed = forms.BooleanField(label="Er opgaven løst", initial=False, required=False)

    class Meta:
        model = Jobs
        fields=["item", "to_do_owner", "completed"]