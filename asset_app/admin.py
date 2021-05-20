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
        "created",
        "last_updated",
        "name",
        "mac_address",
        "serial",
        "purchased_date",
        "may_be_loaned",
        "notes",
        "ip",
    ]
    readonly_fields = [
        "created",
        "last_updated",
        "name",
        "mac_address",
        "serial",
        "purchased_date",
        "may_be_loaned",
        "notes",
        "ip",
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


class Loan_assetAdminForm(forms.ModelForm):
    class Meta:
        model = models.Loan_asset
        fields = "__all__"


class Loan_assetAdmin(admin.ModelAdmin):
    form = Loan_assetAdminForm
    list_display = [
        "loaner_address",
        "last_updated",
        "loaner_name",
        "loaner_quicklink",
        "notes",
        "created",
        "loaner_telephone_number",
        "loaner_email",
        "loan_date",
        "return_date",
    ]
    readonly_fields = [
        "loaner_address",
        "last_updated",
        "loaner_name",
        "loaner_quicklink",
        "notes",
        "created",
        "loaner_telephone_number",
        "loaner_email",
        "loan_date",
        "return_date",
    ]


class LocationsAdminForm(forms.ModelForm):
    class Meta:
        model = models.Locations
        fields = "__all__"


class LocationsAdmin(admin.ModelAdmin):
    form = LocationsAdminForm
    list_display = [
        "address",
        "name",
        "last_updated",
        "created",
        "notes",
    ]
    readonly_fields = [
        "address",
        "name",
        "last_updated",
        "created",
        "notes",
    ]


class Loaner_typeAdminForm(forms.ModelForm):
    class Meta:
        model = models.Loaner_type
        fields = "__all__"


class Loaner_typeAdmin(admin.ModelAdmin):
    form = Loaner_typeAdminForm
    list_display = [
        "created",
        "name",
        "last_updated",
        "notes",
    ]
    readonly_fields = [
        "created",
        "name",
        "last_updated",
        "notes",
    ]


class ModelAdminForm(forms.ModelForm):
    class Meta:
        model = models.Model
        fields = "__all__"


class ModelAdmin(admin.ModelAdmin):
    form = ModelAdminForm
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
        "last_inspected",
        "name",
        "last_updated",
        "image_date",
        "created",
        "image",
        "notes",
    ]
    readonly_fields = [
        "last_inspected",
        "name",
        "last_updated",
        "image_date",
        "created",
        "image",
        "notes",
    ]


admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Asset_type, Asset_typeAdmin)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Loan_asset, Loan_assetAdmin)
admin.site.register(models.Loaner_type, Loaner_typeAdmin)
admin.site.register(models.Locations, LocationsAdmin)
admin.site.register(models.Model, ModelAdmin)
admin.site.register(models.Room, RoomAdmin)
