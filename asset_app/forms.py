from django import forms
from . import models
from .models import Locations, Asset_type, Room, Model_hardware, Asset, Brand, Room_type, Bundle_reservation


class AssetForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udstyrsnavn navn'}))
    serial = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast serie nummer'}))
    model_hardware = forms.ModelChoiceField(queryset=Model_hardware.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    room = forms.ModelChoiceField(queryset=Room.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    purchased_date = forms.DateField(required=False, widget=forms.widgets.DateTimeInput(
        attrs={'class': 'form-control', "type": "date"}))
    mac_address = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast enhedens mac adresse'}))
    ip = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast enhedens ip adresse'}))
    notes = forms.CharField(required=False, label="Noter", max_length=100, widget=forms.Textarea(
        attrs={'class': 'form-control', }))
    may_be_loaned = forms.BooleanField(label="Er rummet brugbar", initial=False, required=False)

    class Meta:
        model = models.Asset
        fields = [
            "name",
            "serial",
            "model_hardware",
            "room",
            "purchased_date",
            "mac_address",
            "ip",
            "notes",
            "may_be_loaned",

        ]


class Asset_typeForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udstyrs type'}))
    notes = forms.CharField(required=False, label="Noter", max_length=100, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Asset_type
        fields = [
            "name",
            "notes",
        ]


class BrandForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast mærke navn'}))
    notes = forms.CharField(required=False, label="Noter", max_length=100, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Brand
        fields = [
            "name",
            "notes",
        ]

class Bundle_reservationForm(forms.ModelForm):
    loaner_name = forms.CharField(label="", max_length=60, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners navn'}))
    location = forms.ModelChoiceField(queryset=Asset.objects.all(), label="Udstyr lånt fra afdeling",
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    loaner_telephone_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners telefon nummer'}))
    loaner_email = forms.EmailField(label="", max_length=100, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners email'}))
    loaner_quicklink = forms.URLField(label="", max_length=100, required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast quicklink'}))
    asset_type = forms.ModelChoiceField(queryset=Asset.objects.all(), label="Udstyr art",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.CharField(label="", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast antal'}))
    series = forms.CharField(label="", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast serie på udstyr'}))
    course_name = forms.CharField(label="", max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast kursus/eller brugs beskrivelse'}))
    loan_date = forms.DateField(required=False, label="Udlåns dato", widget=forms.widgets.DateTimeInput(
        attrs={'class': 'form-control', "type": "date"}))
    return_date = forms.DateField(required=False, label="Afleverings dato", widget=forms.widgets.DateTimeInput(
        attrs={'class': 'form-control', "type": "date"}))
    returned = forms.BooleanField(label="Er udstyret afleveret tilbage", initial=False, required=False)
    notes = forms.CharField(required=False, label="Noter", max_length=100, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Bundle_reservation
        fields = [
            "loaner_name",
            "location",
            "loaner_telephone_number",
            "loaner_email",
            "loaner_quicklink",
            "asset_type",
            "amount",
            "series",
            "course_name",
            "loan_date",
            "return_date",
            "returned",
            "notes",
        ]


class Loan_assetForm(forms.ModelForm):
    loaner_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners navn'}))
    loaner_address = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners adresse'}))
    loaner_telephone_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners telefon nummer'}))
    loaner_email = forms.EmailField(label="", max_length=100, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners email'}))
    loaner_quicklink = forms.URLField(label="", max_length=100, required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast quicklink'}))
    asset = forms.ModelChoiceField(queryset=Asset.objects.all(), label="Udstyr",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    loan_date = forms.DateField(required=False, label="Udlåns dato", widget=forms.widgets.DateTimeInput(
        attrs={'class': 'form-control', "type": "date"}))
    return_date = forms.DateField(required=False, label="Afleverings dato", widget=forms.widgets.DateTimeInput(
        attrs={'class': 'form-control', "type": "date"}))
    returned = forms.BooleanField(label="Er rummet brugbar", initial=False, required=False)
    notes = forms.CharField(required=False, label="Noter", max_length=100, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Loan_asset
        fields = [
            "loaner_name",
            "loaner_address",
            "loaner_quicklink",
            "loaner_telephone_number",
            "loaner_email",
            "asset",
            "loan_date",
            "return_date",
            "returned",
            "notes",
        ]


class Loaner_typeForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast bruger type'}))
    notes = forms.CharField(required=False, label="Noter", max_length=100, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Loaner_type
        fields = [
            "name",
            "notes",
        ]


class LocationsForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast afdelings navn, feks:(POA,MIL,CBV...)'}))
    address = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast afdelings adresse'}))
    notes = forms.CharField(required=False, label="Noter", max_length=100, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Locations
        fields = [
            "name",
            "address",
            "notes",
        ]


class ModelForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast model'}))
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    asset_type = forms.ModelChoiceField(queryset=Asset_type.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    notes = forms.CharField(required=False, label="Noter", max_length=100, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Model_hardware
        fields = [
            "name",
            "brand",
            "asset_type",
            "notes",
        ]


class RoomForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast rum navn'}))
    location = forms.ModelChoiceField(queryset=Locations.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    room_type = forms.ModelChoiceField(queryset=Room_type.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    last_inspected = forms.DateField(required=False, widget=forms.widgets.DateTimeInput(
        attrs={'class': 'form-control', "type": "date"}))
    image_date = forms.DateField(required=False,
                                 widget=forms.widgets.DateTimeInput(attrs={'class': 'form-control', "type": "date"}))
    image = forms.ImageField(required=False, widget=forms.widgets.FileInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(required=False, label="Noter", max_length=100, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Room
        fields = [
            "name",
            "location",
            "room_type",
            "last_inspected",
            "image_date",
            "image",
            "notes",

        ]


class Room_typeForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast rum type'}))
    notes = forms.CharField(required=False, label="Noter", max_length=100, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Room_type
        fields = [
            "name",
            "notes",
        ]
