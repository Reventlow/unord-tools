from rest_framework import serializers
from . import models

class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Asset
        fields = [
            "name",
            "mac_address",
            "ip",
            "purchased_date",
            "serial",
            "created",
            "may_be_loaned",
            "last_updated",
            "notes",
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

class Loaner_typeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Loaner_type
        fields = [
            "created",
            "name",
            "last_updated",
            "notes",
        ]

class ModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Model
        fields = [
            "last_updated",
            "notes",
            "created",
            "name",
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

class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Room
        fields = [
            "image",
            "created",
            "image_date",
            "last_updated",
            "name",
            "last_inspected",
            "notes",
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




