from django.contrib import admin
from django import forms
from . import models


class AssetAdminForm(forms.ModelForm):
    class Meta:
        model = models.Asset
        fields = "__all__"


class AssetAdmin(admin.ModelAdmin):
    form = AssetAdminForm
    list_display = [
        "name",
        "serial",
        "model_hardware",
        "room",
        "purchased_date",
        "mac_address",
        "ip",
        "notes",
        "may_be_loaned",
        "is_loaned",
        "missing",
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]


class Asset_typeAdminForm(forms.ModelForm):
    class Meta:
        model = models.Asset_type
        fields = "__all__"


class Asset_typeAdmin(admin.ModelAdmin):
    form = Asset_typeAdminForm
    list_display = [
        "name",
        "last_updated",
        "created",
        "notes",
    ]
    readonly_fields = [

    ]

class AssetCaseAdminForm(forms.ModelForm):

    class Meta:
        model = models.AssetCase
        fields = "__all__"


class AssetCaseAdmin(admin.ModelAdmin):
    form = AssetCaseAdminForm
    list_display = [
        "description",
        "user_report_it",
        "user_quicklink",
        "zendesk_link",
        "notes",
        "solved",
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]

class AssetLogAdminForm(forms.ModelForm):

    class Meta:
        model = models.AssetLog
        fields = "__all__"

class AssetLogAdmin(admin.ModelAdmin):
    form = AssetLogAdminForm
    list_display = [
        "notes",
        "last_updated",
        "created",
    ]
    readonly_fields = [

    ]


class BrandAdminForm(forms.ModelForm):
    class Meta:
        model = models.Brand
        fields = "__all__"


class BrandAdmin(admin.ModelAdmin):
    form = BrandAdminForm
    list_display = [
        "name",
        "last_updated",
        "created",
        "notes",
    ]
    readonly_fields = [

    ]


class Bundle_reservationAdminForm(forms.ModelForm):
    class Meta:
        model = models.Loan_asset
        fields = "__all__"


class Bundle_reservationAdmin(admin.ModelAdmin):
    form = Bundle_reservationAdminForm
    list_display = [
        "loaner_name",
        "location",
        "loaner_quicklink",
        "loaner_telephone_number",
        "loaner_email",
        "asset_type",
        "amount",
        "series",
        "course_name",
        "loan_date",
        "return_date",
        "returned",
        "notes",
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]


class ExternalServiceAdminForm(forms.ModelForm):

    class Meta:
        model = models.ExternalService
        fields = "__all__"


class ExternalServiceAdmin(admin.ModelAdmin):
    form = ExternalServiceAdminForm
    list_display = [
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
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]

class ExternalServiceContactAdminForm(forms.ModelForm):

    class Meta:
        model = models.ExternalServiceContact
        fields = "__all__"


class ExternalServiceContactAdmin(admin.ModelAdmin):
    form = ExternalServiceContactAdminForm
    list_display = [
        "name",
        "cellphone",
        "email",
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]

class ExternalServicePositionAdminForm(forms.ModelForm):

    class Meta:
        model = models.ExternalServicePosition
        fields = "__all__"


class ExternalServicePositionAdmin(admin.ModelAdmin):
    form = ExternalServicePositionAdminForm
    list_display = [
        "description",
        "notes",
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]


class Loan_assetAdminForm(forms.ModelForm):
    class Meta:
        model = models.Loan_asset
        fields = "__all__"


class Loan_assetAdmin(admin.ModelAdmin):
    form = Loan_assetAdminForm
    list_display = [
        "loaner_name",
        "location",
        "loaner_quicklink",
        "loaner_telephone_number",
        "loaner_email",
        "loaner_type",
        "asset",
        "sms_automatic",
        "eduName",
        "responsible_teacher_initials",
        "responsible_teacher_received_mail",
        "dropped_out_of_school",
        "loan_date",
        "return_date",
        "returned",
        "notes",
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]


class Loaner_typeAdminForm(forms.ModelForm):
    class Meta:
        model = models.Loaner_type
        fields = "__all__"


class Loaner_typeAdmin(admin.ModelAdmin):
    form = Loaner_typeAdminForm
    list_display = [
        "name",
        "notes",
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]


class LocationsAdminForm(forms.ModelForm):
    class Meta:
        model = models.Locations
        fields = "__all__"


class LocationsAdmin(admin.ModelAdmin):
    form = LocationsAdminForm
    list_display = [
        "name",
        "address",
        "notes",
        "created",
        "last_updated",

    ]
    readonly_fields = [

    ]


class Model_hardwareAdminForm(forms.ModelForm):
    class Meta:
        model = models.Model_hardware
        fields = "__all__"


class Model_hadwareAdmin(admin.ModelAdmin):
    form = Model_hardwareAdminForm
    list_display = [
        "name",
        "notes",
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]

class One2OneInfoAdminForm(forms.ModelForm):
    class Meta:
        model = models.One2OneInfo
        fields = "__all__"


class One2OneInfoAdmin(admin.ModelAdmin):
    form = One2OneInfoAdminForm
    list_display = [
        "name",
        "job_owner",
        "completed",
        "notes",
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]


class One2OneInfoLogAdminForm(forms.ModelForm):
    class Meta:
        model = models.One2OneInfoLog
        fields = "__all__"


class One2OneInfoLogAdmin(admin.ModelAdmin):
    form = One2OneInfoLogAdminForm
    list_display = [
        "name",
        "one_2_one_info",
        "location",
        "notes",
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]

class RoomAdminForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = "__all__"


class RoomAdmin(admin.ModelAdmin):
    form = RoomAdminForm
    list_display = [
        "name",
        "location",
        "room_type",
        "last_inspected",
        "image_date",
        "image",
        "notes",
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]


class Room_typeAdminForm(forms.ModelForm):
    class Meta:
        model = models.Room_type
        fields = "__all__"


class Room_typeAdmin(admin.ModelAdmin):
    form = Room_typeAdminForm
    list_display = [
        "name",
        "notes",
        "created",
        "last_updated"
    ]
    readonly_fields = [


    ]

class RoutinesAdminForm(forms.ModelForm):

    class Meta:
        model = models.Routines
        fields = "__all__"


class RoutinesAdmin(admin.ModelAdmin):
    form = RoutinesAdminForm
    list_display = [
        "name",
        "reoccurrence",
        "notes",
        "created",
        "last_updated",
    ]
    readonly_fields = [

    ]


class RoutineLogAdminForm(forms.ModelForm):

    class Meta:
        model = models.RoutineLog
        fields = "__all__"


class RoutineLogAdmin(admin.ModelAdmin):
    form = RoutineLogAdminForm
    list_display = [
        "date",
        "notes",
        "last_updated",
        "created",
    ]
    readonly_fields = [

    ]


class SeverityLevelAdminForm(forms.ModelForm):

    class Meta:
        model = models.SeverityLevel
        fields = "__all__"


class SeverityLevelAdmin(admin.ModelAdmin):
    form = SeverityLevelAdminForm
    list_display = [
        "description",
        "bootstrap_color",
        "sl_level",
        "last_updated",
        "created",
    ]
    readonly_fields = [

    ]

class SmsAdminForm(forms.ModelForm):

    class Meta:
        model = models.Sms
        fields = "__all__"


class SmsAdmin(admin.ModelAdmin):
    form = SmsAdminForm
    list_display = [
        "description",
        "automatic",
        "manual",
        "button_name",
        "button_level",
        "sms_message",
    ]
    readonly_fields = [

    ]

class SmsLogAdminForm(forms.ModelForm):
    class Meta:
        model = models.SmsLog
        fields = "__all__"

class SmsLogAdmin(admin.ModelAdmin):
    form = SmsLogAdminForm
    list_display = [
        "loan_asset",
        "sms",
        "sms_name",
        "sms_number",
        "sms_timestamp",
        "sms_msg_sent",
        "sms_msg_type"
    ]
    readonly_fields = [

    ]


admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Asset_type, Asset_typeAdmin)
admin.site.register(models.AssetCase, AssetCaseAdmin)
admin.site.register(models.AssetLog, AssetLogAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Bundle_reservation, Bundle_reservationAdmin)
admin.site.register(models.ExternalService, ExternalServiceAdmin)
admin.site.register(models.ExternalServiceContact, ExternalServiceContactAdmin)
admin.site.register(models.ExternalServicePosition, ExternalServicePositionAdmin)
admin.site.register(models.Loan_asset, Loan_assetAdmin)
admin.site.register(models.Loaner_type, Loaner_typeAdmin)
admin.site.register(models.Locations, LocationsAdmin)
admin.site.register(models.Model_hardware, Model_hadwareAdmin)
admin.site.register(models.One2OneInfo, One2OneInfoAdmin)
admin.site.register(models.One2OneInfoLog, One2OneInfoLogAdmin)
admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.Room_type, Room_typeAdmin)
admin.site.register(models.Routines, RoutinesAdmin)
admin.site.register(models.RoutineLog, RoutineLogAdmin)
admin.site.register(models.SeverityLevel, SeverityLevelAdmin)
admin.site.register(models.Sms, SmsAdmin)
admin.site.register(models.SmsLog, SmsLogAdmin)
