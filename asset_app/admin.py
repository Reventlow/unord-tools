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
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "name",
        "serial",
        "model_hardware",
        "room",
        "purchased_date",
        "mac_address",
        "ip",
        "notes",
        "may_be_loaned",
        "created",
        "last_updated",
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
        "name",
        "last_updated",
        "created",
        "notes",
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
        "name",
        "last_updated",
        "created",
        "notes",
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


class Loan_assetAdminForm(forms.ModelForm):
    class Meta:
        model = models.Loan_asset
        fields = "__all__"


class Loan_assetAdmin(admin.ModelAdmin):
    form = Loan_assetAdminForm
    list_display = [
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
        "created",
        "last_updated",
    ]
    readonly_fields = [
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
        "created",
        "last_updated",
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
        "name",
        "notes",
        "created",
        "last_updated",
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
        "name",
        "address",
        "notes",
        "created",
        "last_updated",
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
        "name",
        "notes",
        "created",
        "last_updated",
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
        "name",
        "notes",
        "created",
        "last_updated",

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
        "name",
        "reoccurrence",
        "notes",
        "created",
        "last_updated",
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
        "date",
        "notes",
        "last_updated",
        "created",
    ]



admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Asset_type, Asset_typeAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Bundle_reservation, Bundle_reservationAdmin)
admin.site.register(models.Loan_asset, Loan_assetAdmin)
admin.site.register(models.Loaner_type, Loaner_typeAdmin)
admin.site.register(models.Locations, LocationsAdmin)
admin.site.register(models.Model_hardware, Model_hadwareAdmin)
admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.Room_type, Room_typeAdmin)
admin.site.register(models.Routines, RoutinesAdmin)
admin.site.register(models.RoutineLog, RoutineLogAdmin)
