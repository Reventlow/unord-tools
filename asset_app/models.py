from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField

from UnordToolsProject.storage_backends import PublicMediaStorage


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
    is_loaned = models.BooleanField(default=False, blank=True, null=True)
    missing = models.BooleanField(default=False, blank=True, null=True)
    notes = HTMLField(default="")
    ip = models.CharField(max_length=90, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name) + ' | ' + str(self.model_hardware.asset_type) + ' | ' + str(
            self.model_hardware.brand) + ' ' + str(self.model_hardware.name)

    def fourDigitCheck(self):
        thisAsset = str(self.name)
        thisAsset = thisAsset[-4:]
        if thisAsset.isdecimal():
            return thisAsset
        else:
            return str(self.name) + ' | ' + str(self.model_hardware.asset_type) + ' | ' + str(
                self.model_hardware.brand) + ' ' + str(self.model_hardware.name)

    def get_absolute_url(self):
        return reverse("asset_app_asset_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_asset_update", args=(self.pk,))


class Asset_type(models.Model):

    # Fields
    name = models.CharField(max_length=30)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    notes = HTMLField(default="")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_asset_type_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_asset_type_update", args=(self.pk,))

class AssetCase(models.Model):

    # Relationships
    case_owner = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    external_service = models.ForeignKey("asset_app.ExternalService", on_delete=models.SET_NULL, blank=True, null=True)
    asset = models.ForeignKey("asset_app.Asset", on_delete=models.SET_NULL, blank=True, null=True)
    severity_level = models.ForeignKey("asset_app.SeverityLevel", on_delete=models.SET_NULL, null=True)

    # Fields
    description = models.CharField(max_length=60)
    user_report_it = models.CharField(max_length=30, null=True, blank=True)
    user_quicklink = models.URLField(null=True, blank=True)
    zendesk_link = models.URLField(null=True, blank=True)
    solved = models.BooleanField(null=True, blank=True)
    notes = HTMLField(default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)


    class Meta:
        pass

    def __str__(self):
        return str(self.description)

    def get_absolute_url(self):
        return reverse("asset_app_AssetCase_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_AssetCase_update", args=(self.pk,))

class AssetLog(models.Model):

    # Relationships
    log_written_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, blank=True, null=True)
    asset_case = models.ForeignKey("asset_app.AssetCase", on_delete=models.CASCADE)

    # Fields
    notes = HTMLField(default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("asset_app_AssetLog_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_AssetLog_update", args=(self.pk,))

class Brand(models.Model):

    # Fields
    name = models.CharField(max_length=30)
    notes = HTMLField(default="")
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
    notes = HTMLField(default="")
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


class ExternalService(models.Model):

    # Fields
    company_name = models.CharField(max_length=60)
    address_street = models.CharField(max_length=60)
    address_postcode = models.CharField(max_length=30)
    address_city = models.CharField(max_length=30)
    company_telephone = models.CharField(max_length=30)
    company_email = models.CharField(max_length=60)
    company_support_telephone = models.CharField(max_length=30)
    company_support_email = models.CharField(max_length=30)
    company_website = models.URLField(null=True, blank=True)
    notes = HTMLField(default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)




    class Meta:
        pass

    def __str__(self):
        return str(self.company_name)

    def get_absolute_url(self):
        return reverse("asset_app_ExternalService_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_ExternalService_update", args=(self.pk,))

class ExternalServiceContact(models.Model):

    # Relationships
    company = models.ForeignKey("asset_app.ExternalService", on_delete=models.SET_NULL, blank=True, null=True)
    position = models.ForeignKey("asset_app.ExternalServicePosition", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=30)
    cellphone = models.CharField(max_length=30)
    notes = HTMLField(default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)



    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("asset_app_ExternalServiceContact_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_ExternalServiceContact_update", args=(self.pk,))


class ExternalServicePosition(models.Model):

    # Fields
    description = models.CharField(max_length=60)
    notes = HTMLField(default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.description)

    def get_absolute_url(self):
        return reverse("asset_app_ExternalServicePosition_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_ExternalServicePosition_update", args=(self.pk,))




class Loan_asset(models.Model):

    # Relationships
    asset = models.ForeignKey("asset_app.Asset", on_delete=models.SET_NULL, blank=True, null=True)
    loaner_type = models.ForeignKey("asset_app.Loaner_type", on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey("asset_app.Locations", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    loaner_name = models.CharField(max_length=60)
    loaner_telephone_number = models.CharField(max_length=30)
    loaner_email = models.EmailField()
    loaner_quicklink = models.URLField(null=True, blank=True)
    loan_date = models.DateField()
    return_date = models.DateField()
    eduName = models.CharField(max_length=60, blank=True, null=True)
    responsible_teacher_initials = models.CharField(max_length=60, blank=True, null=True)
    responsible_teacher_received_mail = models.BooleanField(default=False, blank=True, null=True)
    endEduDate = models.DateField(blank=True, null=True)
    dropped_out_of_school = models.BooleanField(default=False)
    sms_automatic = models.BooleanField(default=False)
    notes = HTMLField(default="")
    returned = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        pass

    def __str__(self):
        return str(self.loaner_name)

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
    notes = HTMLField(default="")

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
    notes = HTMLField(default="")
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

class One2OneInfo(models.Model):
    # Relationships
    job_owner = models.ForeignKey("auth.User", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    notes = HTMLField(default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["completed","name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("asset_app_one2one_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_one2one_update", args=(self.pk,))

class One2OneInfoLog(models.Model):
    # Relationships
    location = models.ForeignKey("asset_app.Locations", on_delete=models.SET_NULL, blank=True, null=True)
    one_2_one_info = models.ForeignKey("asset_app.One2OneInfo", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    name = models.CharField(max_length=30)
    notes = HTMLField(default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["location","name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("asset_app_one2one_log_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_one2one_log_update", args=(self.pk,))

class Room(models.Model):

    # Relationships
    location = models.ForeignKey("asset_app.Locations",  on_delete=models.SET_NULL, blank=True, null=True)
    room_type = models.ForeignKey("asset_app.Room_type", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields

    name = models.CharField(max_length=30)
    image_date = models.DateField(null=True, blank=True)
    image = models.ImageField(storage=PublicMediaStorage(), null=True, blank=True)
    last_inspected = models.DateField(null=True, blank=True)
    notes = HTMLField(default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)


    class Meta:
        ordering = ["location","name"]

    def __str__(self):
        return str(self.name) + '-' + str(self.location.name)

    def get_absolute_url(self):
        return reverse("asset_app_room_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_room_update", args=(self.pk,))

class Room_type(models.Model):

    # Fields
    name = models.CharField(max_length=30)
    notes = HTMLField(default="")
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




class Routines(models.Model):

    # Relationships
    room = models.ForeignKey("asset_app.Room", on_delete=models.SET_NULL, blank=True, null=True)
    routine_owner = models.ForeignKey("auth.User", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    name = models.CharField(max_length=100)
    reoccurrence = models.IntegerField()
    notes = HTMLField(default="")
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
    routine = models.ForeignKey("asset_app.Routines", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    date = models.DateField()
    notes = HTMLField(default="")
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



class SeverityLevel(models.Model):

    # Fields
    description = models.CharField(max_length=60)
    bootstrap_color = models.CharField(max_length=30)
    sl_level = models.IntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)


    class Meta:
        pass

    def __str__(self):
        return str(self.description)

    def get_absolute_url(self):
        return reverse("asset_app_SeverityLevel_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_SeverityLevel_update", args=(self.pk,))


class Sms(models.Model):

    # Fields
    description = models.CharField(max_length=100)
    automatic = models.BooleanField(default=False)
    manual = models.BooleanField(default=False)
    button_name = models.CharField(max_length=30)
    button_level = models.IntegerField(blank=True, null=True)
    sms_message = models.CharField(max_length=400)

    class Meta:
        pass

    def __str__(self):
        return str(self.description)

    def get_absolute_url(self):
        return reverse("asset_app_sms_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("asset_app_sms_update", args=(self.pk,))


class SmsLog(models.Model):
    # Relationships
    loan_asset = models.ForeignKey("asset_app.Loan_asset", on_delete=models.SET_NULL, blank=True, null=True)
    sms = models.ForeignKey("asset_app.Sms", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    sms_name = models.CharField(max_length=60)
    sms_number = models.CharField(max_length=8)
    sms_timestamp = models.DateTimeField()
    sms_msg_sent = models.CharField(max_length=400)
    sms_msg_type = models.CharField(max_length=20)


    class Meta:
        pass

    def __str__(self):
        return str(self.sms_timestamp)
