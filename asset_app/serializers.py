from rest_framework import serializers
from . import models

class AssetSerializer(serializers.ModelSerializer):

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
            "is_loaned",
            "missing",
            "created",
            "last_updated",
        ]


class Asset_typeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Asset_type
        fields = [
            "notes",
            "name",
            "created",
            "last_updated",

        ]

class AssetCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AssetCase
        fields = [
            "description",
            "user_report_it",
            "user_quicklink",
            "zendesk_link",
            "notes",
            "solved",
            "created",
            "last_updated",
        ]

class AssetLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AssetLog
        fields = [
            "notes",
            "last_updated",
            "created",

        ]

class Bundle_reservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Asset_type
        fields = [
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

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Brand
        fields = [
            "notes",
            "name",
            "created",
            "last_updated",

        ]


class ExternalServiceSerializer(serializers.ModelSerializer):

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
            "created",
            "last_updated",
        ]

class ExternalServiceContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ExternalServiceContact
        fields = [
            "name",
            "cellphone",
            "email",
            "created",
            "last_updated",
        ]

class ExternalServicePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExternalServicePosition
        fields = [
            "description",
            "notes",
            "created",
            "last_updated",
        ]

class Loan_assetSerializer(serializers.ModelSerializer):

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
            "sms_automatic",
            "eduName",
            "loan_date",
            "return_date",
            "returned",
            "notes",
            "created",
            "last_updated",
        ]

class Loaner_typeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Loaner_type
        fields = [
            "created",
            "name",
            "last_updated",
            "notes",
        ]


class LocationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Locations
        fields = [
            "last_updated",
            "address",
            "created",
            "name",
            "notes",
        ]

class Model_hardwareSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Model_hardware
        fields = [
            "last_updated",
            "notes",
            "created",
            "name",
        ]

class One2OneInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.One2OneInfo
        fields = [
        "name",
        "job_owner",
        "completed",
        "notes",
        "created",
        "last_updated",
        ]

class One2OneInfoLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.One2OneInfoLog
        fields = [
        "name",
        "job_owner",
        "one_2_one_info",
        "locations",
        "notes",
        "created",
        "last_updated",
        ]


class RoomSerializer(serializers.ModelSerializer):

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
            "created",
            "last_updated",
        ]

class Room_typeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Room_type
        fields = [
            "notes",
            "name",
            "created",
            "last_updated",

        ]

class RoutinesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Routines
        fields = [
            "Reoccurrence",
            "name",
            "notes",
            "created",
            "last_updated",
        ]

class RoutineLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RoutineLog
        fields = [
            "last_updated",
            "created",
            "notes",
            "date",
        ]


class SeverityLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SeverityLevel
        fields = [
            "description",
            "bootstrap_color",
            "sl_level",
            "last_updated",
            "created",

        ]

class SmsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SeverityLevel
        fields = [
            "description",
            "automatic",
            "manual",
            "button_name",
            "button_level",
            "sms_message",

        ]

class SmsLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SeverityLevel
        fields = [
            "loan_asset",
            "sms",
            "sms_name",
            "sms_number",
            "sms_timestamp",
            "sms_msg_sent",
            "sms_msg_type"

        ]