from django.contrib import admin
from django import forms

from . import models


class locationsAdminForm(forms.ModelForm):

    class Meta:
        model = models.Locations
        fields = "__all__"


class locationsAdmin(admin.ModelAdmin):
    form = locationsAdminForm
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


class asset_typeAdminForm(forms.ModelForm):

    class Meta:
        model = models.Asset_type
        fields = "__all__"


class asset_typeAdmin(admin.ModelAdmin):
    form = asset_typeAdminForm
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


class loan_assetAdminForm(forms.ModelForm):

    class Meta:
        model = models.Loan_asset
        fields = "__all__"


class loan_assetAdmin(admin.ModelAdmin):
    form = loan_assetAdminForm
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


class roomAdminForm(forms.ModelForm):

    class Meta:
        model = models.Room
        fields = "__all__"


class roomAdmin(admin.ModelAdmin):
    form = roomAdminForm
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


class assetAdminForm(forms.ModelForm):

    class Meta:
        model = models.Asset
        fields = "__all__"


class assetAdmin(admin.ModelAdmin):
    form = assetAdminForm
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


class loaner_typeAdminForm(forms.ModelForm):

    class Meta:
        model = models.Loaner_type
        fields = "__all__"


class loaner_typeAdmin(admin.ModelAdmin):
    form = loaner_typeAdminForm
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


class modelAdminForm(forms.ModelForm):

    class Meta:
        model = models.Model
        fields = "__all__"


class modelAdmin(admin.ModelAdmin):
    form = modelAdminForm
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


admin.site.register(models.Locations, locationsAdmin)
admin.site.register(models.Asset_type, asset_typeAdmin)
admin.site.register(models.Loan_asset, loan_assetAdmin)
admin.site.register(models.Room, roomAdmin)
admin.site.register(models.Asset, assetAdmin)
admin.site.register(models.Loaner_type, loaner_typeAdmin)
admin.site.register(models.Model, modelAdmin)