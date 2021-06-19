from django.contrib import admin
from django import forms
from . import models

# Register your models here.

class JobsAdminForm(forms.ModelForm):

    class Meta:
        model = models.Jobs
        fields = "__all__"

class JobsAdmin(admin.ModelAdmin):
    form = JobsAdminForm
    list_display = ["item", "to_do_owner", "completed"]
    readonly_fields = ["item", "to_do_owner", "completed"]

admin.site.register(models.Jobs, JobsAdmin)
