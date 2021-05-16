from rest_framework import serializers

from . import models


class locationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Locations
        fields = [
            "last_updated",
            "address",
            "created",
            "name",
            "notes",
        ]

class asset_typeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Asset_type
        fields = [
            "notes",
            "name",
            "created",
            "last_updated",

        ]

class loan_assetSerializer(serializers.ModelSerializer):

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

class roomSerializer(serializers.ModelSerializer):

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

class assetSerializer(serializers.ModelSerializer):

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

class loaner_typeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Loaner_type
        fields = [
            "created",
            "name",
            "last_updated",
            "notes",
        ]

class modelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Model
        fields = [
            "last_updated",
            "notes",
            "created",
            "name",
        ]
