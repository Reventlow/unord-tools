from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Locations, Asset_type, Room, Model_hardware, Asset, Brand, Room_type, Loaner_type, Routines, One2OneInfo


class AssetForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udstyrsnavn navn'}))
    serial = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast serie nummer'}))
    model_hardware = forms.ModelChoiceField(queryset=Model_hardware.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    room = forms.ModelChoiceField(queryset=Room.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    purchased_date = forms.DateField(required=False, widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control', "type": "date"}))
    mac_address = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast enhedens mac adresse'}))
    ip = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast enhedens ip adresse'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=forms.Textarea(
        attrs={'class': 'form-control', }))
    may_be_loaned = forms.BooleanField(label="Må udstyret udlånes", initial=False, required=False)

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
    location = forms.ModelChoiceField(queryset=Locations.objects.all(), label="Udstyr lånt fra afdeling",
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    loaner_telephone_number = forms.CharField(label="",required=False, max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners telefon nummer'}))
    loaner_email = forms.EmailField(label="", max_length=100, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners email'}))
    loaner_quicklink = forms.URLField(label="", max_length=100, required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast quicklink'}))
    asset_type = forms.ModelChoiceField(queryset=Asset_type.objects.all(), label="Udstyr art",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.CharField(label="", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast antal'}))
    series = forms.CharField(label="", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast serie på udstyr'}))
    course_name = forms.CharField(label="", max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast kursus/eller brugs beskrivelse'}))
    loan_date = forms.DateField(required=False, label="Udlåns dato", widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control', "type": "date"}))
    return_date = forms.DateField(required=False, label="Afleverings dato", widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
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
    location = forms.ModelChoiceField(queryset=Locations.objects.all(), label="Udstyr lånt fra afdeling",
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    loaner_address = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners adresse'}))
    loaner_telephone_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners telefon nummer'}))
    loaner_email = forms.EmailField(label="", max_length=100, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners email'}))
    loaner_quicklink = forms.URLField(label="", max_length=100, required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast quicklink'}))
    loaner_type = forms.ModelChoiceField(queryset=Loaner_type.objects.all(), label="Udlåner",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    asset = forms.ModelChoiceField(queryset=Asset.objects.filter(may_be_loaned=True), label="Udstyr",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    loan_date = forms.DateField(required=False, label="Udlåns dato", widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control', "type": "date"}))
    return_date = forms.DateField(required=False, label="Afleverings dato", widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control', "type": "date"}))
    returned = forms.BooleanField(label="Er udstyret retuneret", initial=False, required=False)
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Loan_asset
        fields = [
            "loaner_name",
            "location",
            "loaner_address",
            "loaner_quicklink",
            "loaner_telephone_number",
            "loaner_email",
            "loaner_type",
            "asset",
            "loan_date",
            "return_date",
            "returned",
            "notes",
        ]


class Loaner_typeForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast bruger type'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=forms.Textarea(
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
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=forms.Textarea(
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
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Model_hardware
        fields = [
            "name",
            "brand",
            "asset_type",
            "notes",
        ]

class One2OneInfoForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast opgave beskrivelse'}))
    completed = forms.BooleanField(label="Er opgaven udført", initial=False, required=False)
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.One2OneInfo
        fields = [
            "name",
            "completed",
            "notes",

        ]


class One2OneInfoLogForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Brugernavn'}))
    one_2_one_info = forms.ModelChoiceField(queryset=One2OneInfo.objects.filter(completed=False),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.ModelChoiceField(queryset=Locations.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.One2OneInfoLog
        fields = [
            "name",
            "one_2_one_info",
            "location",
            "notes",
        ]


class RoomForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast rum navn'}))
    location = forms.ModelChoiceField(queryset=Locations.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    room_type = forms.ModelChoiceField(queryset=Room_type.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    last_inspected = forms.DateField(required=False, widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control', "type": "date"}))
    image_date = forms.DateField(required=False, widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control', "type": "date"}))
    image = forms.ImageField(required=False, widget=forms.widgets.FileInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=forms.Textarea(
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
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Room_type
        fields = [
            "name",
            "notes",
        ]

class RoutinesForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast routine beskrivelse'}))
    reoccurrence = forms.IntegerField(required=True, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Gentages efter antale dage'}))
    room = forms.ModelChoiceField(queryset=Room.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    routine_owner = forms.ModelChoiceField(queryset=User.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=forms.Textarea(
        attrs={'class': 'form-control', }))

    class Meta:
        model = models.Routines
        fields = [
            "name",
            "reoccurrence",
            "room",
            "routine_owner",
            "notes",
        ]

class RoutineLogForm(forms.ModelForm):
    date = forms.DateField(required=False, widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
                                                                                        attrs={'class': 'form-control',
                                                                                               "type": "date"}))
    routine = forms.ModelChoiceField(queryset=Routines.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=forms.Textarea(
        attrs={'class': 'form-control', }))
    class Meta:
        model = models.RoutineLog
        fields = [
            "date",
            "routine",
            "notes",
        ]
