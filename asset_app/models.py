from django.db import models
from django.urls import reverse
from django.conf import settings

from UnordToolsProject.storage_backends import PublicMediaStorage, PrivateMediaStorage


class Asset(models.Model):

    # Relationships
    room = models.ForeignKey("asset_app.Room", on_delete=models.SET_NULL, blank=True, null=True)
    model_hardware = models.ForeignKey("asset_app.Model_hardware", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    name = models.CharField(max_length=30)
    serial = models.CharField(max_length=30, unique=True, blank=True, null=True, default=None)
    mac_address = models.CharField(max_length=30, null=True, blank=True)
    purchased_date = models.DateField(null=True, blank=True)
    may_be_loaned = models.BooleanField(default=False, blank=True, null=True)
    notes = models.TextField(max_length=448, null=True, blank=True)
    ip = models.CharField(max_length=90, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_asset_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_asset_update", args=(self.pk,))


class Asset_type(models.Model):

    # Fields
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    notes = models.TextField(max_length=448, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_asset_type_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_asset_type_update", args=(self.pk,))

class Brand(models.Model):

    # Fields
    name = models.CharField(max_length=30)
    notes = models.TextField(max_length=448, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_brand_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_brand_update", args=(self.pk,))

class Bundle_reservation(models.Model):
    # Relationships
    asset_type = models.ForeignKey("asset_app.Asset_type", on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey("asset_app.Locations", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    loaner_name = models.CharField(max_length=60)
    loaner_email = models.EmailField()
    loaner_telephone_number = models.CharField(max_length=30)
    loaner_quicklink = models.URLField(null=True, blank=True)
    amount = models.IntegerField()
    series = models.CharField(max_length=60, null=True, blank=True)
    course_name = models.CharField(max_length=30, null=True, blank=True)
    loan_date = models.DateField()
    return_date = models.DateField()
    returned = models.BooleanField(default=False, blank=True, null=True)
    notes = models.TextField(max_length=448, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["-return_date"]

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("asset_app_bundle_reservation_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_bundle_reservation_update", args=(self.pk,))



class Loan_asset(models.Model):

    # Relationships
    asset = models.ForeignKey("asset_app.Asset", on_delete=models.SET_NULL, blank=True, null=True)
    loaner_type = models.ForeignKey("asset_app.Loaner_type", on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey("asset_app.Locations", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    loaner_name = models.CharField(max_length=60)
    loaner_address = models.TextField(max_length=100, null=True, blank=True)
    loaner_telephone_number = models.CharField(max_length=30)
    loaner_email = models.EmailField()
    loaner_quicklink = models.URLField(null=True, blank=True)
    loan_date = models.DateField()
    return_date = models.DateField()
    notes = models.TextField(max_length=448, null=True, blank=True)
    returned = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("asset_app_loan_asset_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_loan_asset_update", args=(self.pk,))

class Loaner_type(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    notes = models.TextField(max_length=448, null=True, blank=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_loaner_type_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_loaner_type_update", args=(self.pk,))

class Locations(models.Model):

    # Fields
    address = models.CharField(max_length=60, null=True, blank=True)
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    notes = models.TextField(max_length=448, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_locations_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_locations_update", args=(self.pk,))

class Model_hardware(models.Model):

    # Relationships
    asset_type = models.ForeignKey("asset_app.Asset_type", on_delete=models.SET_NULL, blank=True, null=True)
    brand = models.ForeignKey("asset_app.Brand", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    name = models.CharField(max_length=60)
    notes = models.TextField(max_length=448, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_model_hardware_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_model_hardware_update", args=(self.pk,))

class Room(models.Model):

    # Relationships
    location = models.ForeignKey("asset_app.Locations",  on_delete=models.SET_NULL, blank=True, null=True)
    room_type = models.ForeignKey("asset_app.Room_type", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields

    name = models.CharField(max_length=30)
    image_date = models.DateField(null=True, blank=True)
    image = models.ImageField(storage=PublicMediaStorage(), null=True, blank=True)
    last_inspected = models.DateField(null=True, blank=True)
    notes = models.TextField(max_length=448, null=True, blank=True, default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)


    class Meta:
        ordering = ["location","name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("asset_app_room_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_room_update", args=(self.pk,))

class Room_type(models.Model):

    # Fields
    name = models.CharField(max_length=30)
    notes = models.TextField(max_length=448, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_room_type_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_room_type_update", args=(self.pk,))

from django.db import models
from django.urls import reverse


class Routines(models.Model):

    # Relationships
    room = models.ForeignKey("asset_app.Room", on_delete=models.SET_NULL, blank=True, null=True)
    routine_owner = models.ForeignKey("auth.User", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    name = models.CharField(max_length=100)
    reoccurrence = models.IntegerField()
    notes = models.TextField(max_length=448)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_routines_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_routines_update", args=(self.pk,))

class RoutineLog(models.Model):

    # Relationships
    routine = models.ForeignKey("asset_app.routines", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    date = models.DateField()
    notes = models.TextField(max_length=448)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)



    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("asset_app_routineLog_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_routineLog_update", args=(self.pk,))






