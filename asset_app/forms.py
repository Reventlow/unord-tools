from django import forms
from . import models
from .models import Locations
from .widgets import BootstrapDateTimePickerInput


class locationsForm(forms.ModelForm):
    class Meta:
        model = models.Locations
        fields = [
            "address",
            "name",
            "notes",
        ]


class asset_typeForm(forms.ModelForm):
    class Meta:
        model = models.Asset_type
        fields = [
            "name",
            "notes",
        ]


class loan_assetForm(forms.ModelForm):
    class Meta:
        model = models.Loan_asset
        fields = [
            "loaner_address",
            "loaner_name",
            "loaner_quicklink",
            "notes",
            "loaner_telephone_number",
            "loaner_email",
            "loan_date",
            "return_date",
            "asset",
        ]


class roomForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast fornavn'}))
    location = forms.ModelChoiceField(queryset=Locations.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    last_inspected = forms.DateField(required=False, widget=forms.widgets.DateTimeInput(attrs={'class': 'form-control',"type": "date"}))
    image_date = forms.DateField(required=False, widget=forms.widgets.DateTimeInput(attrs={'class': 'form-control',"type": "date"}))
    image = forms.ImageField(required=False, widget=forms.widgets.FileInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(required=False, label="Noter", max_length=100,  widget=forms.Textarea(
        attrs={'class': 'form-control', }))


    class Meta:
        model = models.Room
        fields = [
            "name",
            "location",
            "last_inspected",
            "image_date",
            "image",
            "notes",

        ]


class assetForm(forms.ModelForm):
    class Meta:
        model = models.Asset
        fields = [
            "name",
            "mac_address",
            "serial",
            "purchased_date",
            "may_be_loaned",
            "notes",
            "ip",
            "room",
            "asset_type",
            "model",
        ]


class loaner_typeForm(forms.ModelForm):
    class Meta:
        model = models.Loaner_type
        fields = [
            "name",
            "notes",
        ]


class modelForm(forms.ModelForm):
    class Meta:
        model = models.Model
        fields = [
            "name",
            "notes",
            "asset_type",
        ]