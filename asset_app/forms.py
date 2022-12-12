from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Locations, Asset_type, Room, Model_hardware, Asset, Brand, Room_type, Loaner_type, Routines, One2OneInfo, SeverityLevel, ExternalService, AssetCase, ExternalServicePosition, Loan_asset, Sms
from tinymce.widgets import TinyMCE
from django.db.models import Q
from datetime import date, timedelta


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

# function to get date 1 month from today
def date_1_month_from_now():
    today = date.today()
    return today + timedelta(days=30)




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
    notes = forms.CharField(required=False, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))
    may_be_loaned = forms.BooleanField(label="Må udstyret udlånes", initial=False, required=False)
    is_loaned = forms.BooleanField(label="Er udstyret udlånt nu", initial=False, required=False)
    missing = forms.BooleanField(label="Udstyret meldt savnede", initial=False, required=False)

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
            "may_be_loaned",
            "notes",
            "is_loaned",
            "missing",

        ]


class Asset_typeForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udstyrs type'}))
    notes = forms.CharField(required=False, label="Noter", max_length=100, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

    class Meta:
        model = models.Asset_type
        fields = [
            "name",
            "notes",
        ]

class AssetCaseForm(forms.ModelForm):
    description = forms.CharField(label="", max_length=60, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast emne til fejlmelding'}))
    case_owner = forms.ModelChoiceField(queryset=User.objects.all(), label="Ansvarlig for sagen",
                                            widget=forms.Select(attrs={'class': 'form-control'}))
    asset = forms.ModelChoiceField(queryset=Asset.objects.all().order_by('model_hardware__asset_type__name','name'), label="Udstyr påvirket af fejl",
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    severity_level = forms.ModelChoiceField(queryset=SeverityLevel.objects.all().order_by('-sl_level'), label="Påvirket af fejl",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    user_report_it = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Bruger der har anmeldt fejlen'}))
    user_quicklink = forms.URLField(label="", max_length=100, required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast quicklink til brugeren'}))
    zendesk_link = forms.URLField(label="", max_length=100, required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast quicklink til zendesk sag'}))
    external_service = forms.ModelChoiceField(queryset=ExternalService.objects.all(), required=False,
                                            widget=forms.Select(attrs={'class': 'form-control'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))
    solved = forms.BooleanField(label="Er sagen løst", initial=False, required=False)


    class Meta:
        model = models.AssetCase
        fields = [
            "description",
            "case_owner",
            "asset",
            "severity_level",
            "user_report_it",
            "user_quicklink",
            "zendesk_link",
            "external_service",
            "notes",
            "solved",
        ]

class AssetLogForm(forms.ModelForm):
    asset_case = forms.ModelChoiceField(queryset=AssetCase.objects.all(), label="Sagen den omhandler",
                                            widget=forms.Select(attrs={'class': 'form-control'}))
    log_written_by = forms.CharField(widget=forms.HiddenInput())
    notes = forms.CharField(required=False, label="Noter", max_length=1024, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))


    class Meta:
        model = models.AssetLog
        fields = [
            "asset_case",
            "log_written_by",
            "notes",
        ]

class BrandForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast mærke navn'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

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
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

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

class ExternalServiceForm(forms.ModelForm):
    company_name = forms.CharField(label="", max_length=60, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast firma navn'}))
    address_street = forms.CharField(label="", required=False, max_length=60, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast firma adresse'}))
    address_postcode = forms.CharField(label="", required=False, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast firma post nummer'}))
    address_city = forms.CharField(label="", required=False,  max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast firma by'}))
    company_telephone = forms.CharField(label="", required=False, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast firma telefon nummer'}))
    company_email = forms.CharField(label="", required=False, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast firma email'}))
    company_support_telephone = forms.CharField(label="", required=False, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast firma support nummer'}))
    company_support_email = forms.CharField(label="", required=False, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast firma support email'}))
    company_website = forms.CharField(label="", required=False, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast firma webside'}))
    notes = forms.CharField(required=False, label="Noter", widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

    class Meta:
        model = models.ExternalService
        fields = [
            "company_name",
            "address_street",
            "address_postcode",
            "address_city",
            "company_telephone",
            "company_email",
            "company_website",
            "company_support_telephone",
            "company_support_email",
            "notes",
        ]

class ExternalServiceContactForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=60, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast kontaktpersons navn'}))
    company = forms.ModelChoiceField(queryset=ExternalService.objects.all(), label="Firma",
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    position = forms.ModelChoiceField(queryset=ExternalServicePosition.objects.all(), label="Stilling",
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    cellphone = forms.CharField(label="", required=False, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast kontakt nummer'}))
    email = forms.CharField(label="", required=False, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast email'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

    class Meta:
        model = models.ExternalServiceContact
        fields = [
            "name",
            "position",
            "company",
            "cellphone",
            "email",
        ]


class ExternalServicePositionForm(forms.ModelForm):
    description = forms.CharField(label="", max_length=60, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast stillings betegnelse'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))
    class Meta:
        model = models.ExternalServicePosition
        fields = [
            "description",
            "notes",
        ]


class Loan_assetForm(forms.ModelForm):
    loaner_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners navn'}))
    location = forms.ModelChoiceField(queryset=Locations.objects.all(), label="Udstyr lånt fra afdeling",
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    loaner_telephone_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners telefon nummer'}))
    loaner_email = forms.EmailField(label="", max_length=100, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners email'}))
    loaner_quicklink = forms.URLField(label="", max_length=100, required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast quicklink'}))
    loaner_type = forms.ModelChoiceField(queryset=Loaner_type.objects.all(), label="Udlåner",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    asset = forms.ModelChoiceField(
                                   queryset=Asset.objects.filter(Q(is_loaned=False) & Q(may_be_loaned=True)),
                                   label="Udstyr",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    eduName = forms.CharField(required=False, label="", max_length=60, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Hvis elev/kursist mulighed for at skrive uddannelse'}))
    endEduDate = forms.DateField(required=False, label="Hvis elev/kursist mulighed for at skrive slut studie dato", widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
                                                                                        attrs={'class': 'form-control',
                                                                                               "type": "date"}))
    responsible_teacher_initials = forms.CharField(required=False, label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast ansvalig læres initialier'}))
    responsible_teacher_received_mail = forms.BooleanField(label="Underviser har modtaget mail om at elev skal huske at aflever", initial=False, required=False, disabled=True)
    dropped_out_of_school = forms.BooleanField(label="Er ikke længer tilknyttet skolen", initial=False, required=False)
    loan_date = forms.DateField(label="Udlåns dato", widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control', "type": "date"}))
    return_date = forms.DateField(label="Afleverings dato", widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control', "type": "date"}))
    sms_automatic = forms.BooleanField(label="Send sms automatisk", initial=False, required=False)

    returned = forms.BooleanField(label="Er udstyret returneret", initial=False, required=False)
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

    class Meta:
        model = models.Loan_asset
        fields = [
            "loaner_name",
            "location",
            "loaner_quicklink",
            "loaner_telephone_number",
            "loaner_email",
            "loaner_type",
            "asset",
            "eduName",
            "endEduDate",
            "responsible_teacher_initials",
            "responsible_teacher_received_mail",
            "dropped_out_of_school",
            "loan_date",
            "return_date",
            "sms_automatic",
            "returned",
            "notes",
        ]

    def clean_loaner_name(self):
        return self.cleaned_data['loaner_name']

    def clean_asset(self):
        return self.cleaned_data['asset']

    def clean_loaner_type(self):
        return self.cleaned_data['loaner_type']

    def clean_loaner_telephone_number(self):
        if str.isdecimal(self.cleaned_data['loaner_telephone_number']):
            return self.cleaned_data['loaner_telephone_number']
        else:
            return 0

    def clean_loaner_email(self):
        return self.cleaned_data['loaner_email']

    def clean_loan_date(self):
        return self.cleaned_data['loan_date']

    def clean_return_date(self):
        return self.cleaned_data['return_date']

    #def clean_location(self):
    #    if self.cleaned_data['location'] == '1':
    #        return "Carlsbergvej 34, 3400 Hillerød"
    #    elif self.cleaned_data['location'] == '2':
    #        return "Peder Oxes Allé 4, 3400 Hillerød"
    #    elif self.cleaned_data['location'] == '3':
    #        return "Milnersvej 48, 3400 Hillerød"
    #    else:
    #        return "på den U/Nord afdeling du går på"




class Loan_assetUpdateForm(forms.ModelForm):
    loaner_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners navn'}))
    location = forms.ModelChoiceField(queryset=Locations.objects.all(), label="Udstyr lånt fra afdeling",
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    loaner_telephone_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners telefon nummer'}))
    loaner_email = forms.EmailField(label="", max_length=100, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast udlåners email'}))
    loaner_quicklink = forms.URLField(label="", max_length=100, required=False, widget=forms.URLInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast quicklink'}))
    loaner_type = forms.ModelChoiceField(queryset=Loaner_type.objects.all(), label="Udlåner",
                                   widget=forms.Select(attrs={'class': 'form-control'}))

    asset = forms.ModelChoiceField(queryset=Asset.objects.all(), label="Udstyr", widget=forms.HiddenInput())
    eduName = forms.CharField(required=False, label="", max_length=60, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Hvis elev/kursist, mulighed for at skrive uddannelse'}))
    endEduDate = forms.DateField(required=False, label="Hvis elev/kursist, mulighed for at skrive slut studie dato",
                                 widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
                                                                    attrs={'class': 'form-control',
                                                                           "type": "date"}))
    responsible_teacher_initials = forms.CharField(required=False, label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast ansvalig læres initialier'}))
    responsible_teacher_received_mail = forms.BooleanField(
        label="Underviser har modtaget mail om at elev skal huske at aflever", initial=False, required=False,
        disabled=True)

    dropped_out_of_school = forms.BooleanField(label="Er ikke længer tilknyttet skolen", initial=False, required=False)
    loan_date = forms.DateField(label="Udlåns dato", widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control', "type": "date"}))
    return_date = forms.DateField(label="Afleverings dato", widget=forms.widgets.DateTimeInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control', "type": "date"}))
    returned = forms.BooleanField(label="Er udstyret returneret", initial=False, required=False)
    sms_automatic = forms.BooleanField(label="Send sms automatisk", initial=False, required=False)

    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

    class Meta:
        model = models.Loan_asset
        fields = [
            "loaner_name",
            "location",
            "loaner_quicklink",
            "loaner_telephone_number",
            "loaner_email",
            "loaner_type",
            "asset",
            "eduName",
            "endEduDate",
            "dropped_out_of_school",
            "loan_date",
            "return_date",
            "sms_automatic",
            "returned",
            "notes",
        ]


class Loaner_typeForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast bruger type'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

    class Meta:
        model = models.Loaner_type
        fields = [
            "name",
            "notes",
        ]


class LocationsForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast afdelings navn, f.eks.:(POA,MIL,CBV...)'}))
    address = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast afdelings adresse'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

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
    notes = forms.CharField(required=False, label="Noter", max_length=10000, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

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
    job_owner = forms.ModelChoiceField(queryset=User.objects.all(),
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    completed = forms.BooleanField(label="Er opgaven udført", initial=False, required=False)
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

    class Meta:
        model = models.One2OneInfo
        fields = [
            "name",
            "job_owner",
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
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

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
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

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
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

    class Meta:
        model = models.Room_type
        fields = [
            "name",
            "notes",
        ]

class RoutinesForm(forms.ModelForm):
    name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast routine beskrivelse'}))
    reoccurrence = forms.IntegerField(required=True, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Gentages efter antal dage'}))
    room = forms.ModelChoiceField(queryset=Room.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    routine_owner = forms.ModelChoiceField(queryset=User.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    notes = forms.CharField(required=False, label="Noter", max_length=448, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))

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
    notes = forms.CharField(required=False, label="Noter", max_length=2096, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))
    class Meta:
        model = models.RoutineLog
        fields = [
            "date",
            "routine",
            "notes",
        ]

class SeverityLevelForm(forms.ModelForm):
    description = forms.CharField(label="", max_length=60, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast påvirkning'}))
    bootstrap_color = forms.CharField(label="", max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Indtast bootstrap farve'}))
    sl_level= forms.IntegerField(required=True, label="", min_value=1, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Påvirknings grad 1 er max'}))
    class Meta:
        model = models.SeverityLevel
        fields = [
            "description",
            "bootstrap_color",
            "sl_level",
        ]

class SmsForm(forms.ModelForm):
    description = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Indtern SMS navn'}))
    button_name = forms.CharField(label="", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sms knap navn'}))
    button_level = forms.IntegerField(required=True, label="", min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Knap rækkefølge'}))
    automatic = forms.BooleanField(label="Send sms automatisk", initial=False, required=False)
    manual = forms.BooleanField(label="Sms knap", initial=False, required=False)
    sms_message = forms.CharField(required=False, label="Sms besked", max_length=400, widget=forms.Textarea(attrs={'class': 'form-control'}))


    class Meta:
        model = models.Sms
        fields = [
            "description",
            "automatic",
            "manual",
            "button_name",
            "button_level",
            "sms_message",
        ]

class SmsLogForm(forms.ModelForm):
    loan_asset = forms.ModelChoiceField(queryset=Loan_asset.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    location = forms.ModelChoiceField(queryset=Sms.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    sms_name = forms.CharField(label="", max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Navn på udlåner'}))
    sms_number = forms.CharField(label="", max_length=8, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Udlåner mobil nummer'}))
    sms_timestamp = forms.DateField(label="Sms sendt:", required=False, widget=forms.widgets.DateTimeInput(format=('%d/%m/%Y %H:%M:%S'), attrs={'class': 'form-control', "type": "datetime"}))
    sms_msg_sent = forms.CharField(required=False, label="Sms besked", max_length=400, widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))
    sms_msg_type = forms.CharField(label="", max_length=8, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sms type'}))


    class Meta:
        model = models.SmsLog
        fields = [
            "loan_asset",
            "sms",
            "sms_name",
            "sms_number",
            "sms_timestamp",
            "sms_msg_sent",
            "sms_msg_type"
        ]

