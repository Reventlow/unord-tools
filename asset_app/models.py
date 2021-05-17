from django.db import models
from django.urls import reverse


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


class Asset_type(models.Model):

    # Fields
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    notes = models.TextField(max_length=448, null=True, blank=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_asset_type_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_asset_type_update", args=(self.pk,))


class Loan_asset(models.Model):

    # Relationships
    asset = models.ForeignKey("asset_app.Asset", on_delete=models.CASCADE)

    # Fields
    loaner_address = models.TextField(max_length=100, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    loaner_name = models.CharField(max_length=60)
    loaner_quicklink = models.URLField(null=True, blank=True)
    notes = models.TextField(max_length=448, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    loaner_telephone_number = models.CharField(max_length=30)
    loaner_email = models.EmailField()
    loan_date = models.DateField()
    return_date = models.DateField()

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("asset_app_loan_asset_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_loan_asset_update", args=(self.pk,))


class Room(models.Model):

    # Relationships
    location = models.ForeignKey("asset_app.Locations", related_name="%(class)s_requests_created", on_delete=models.CASCADE, default=1)

    # Fields
    last_inspected = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    image_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    image = models.ImageField(null=True, blank=True)
    notes = models.TextField(max_length=448, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("asset_app_room_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_room_update", args=(self.pk,))


class Asset(models.Model):

    # Relationships
    room = models.ForeignKey("asset_app.Room", on_delete=models.CASCADE)
    asset_type = models.ForeignKey("asset_app.Asset_type", on_delete=models.CASCADE)
    model = models.ForeignKey("asset_app.Model", on_delete=models.CASCADE)

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    name = models.CharField(max_length=30)
    mac_address = models.CharField(max_length=30, null=True, blank=True)
    serial = models.CharField(max_length=30, null=True, blank=True)
    purchased_date = models.DateField(null=True, blank=True)
    may_be_loaned = models.BooleanField(default=False)
    notes = models.TextField(max_length=448, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_asset_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_asset_update", args=(self.pk,))


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


class Model(models.Model):

    # Relationships
    asset_type = models.ForeignKey("asset_app.Asset_type", on_delete=models.CASCADE)

    # Fields
    name = models.CharField(max_length=30)
    notes = models.TextField(max_length=448, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_model_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_model_update", args=(self.pk,))