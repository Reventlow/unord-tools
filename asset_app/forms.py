from django import forms
from . import models


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
    class Meta:
        model = models.Room
        fields = [
            "last_inspected",
            "name",
            "image_date",
            "image",
            "notes",
            "location",
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