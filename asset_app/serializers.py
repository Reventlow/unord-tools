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

class Loan_assetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Loan_asset
        fields = [
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




