from rest_framework import viewsets, permissions

from . import serializers
from . import models


class AssetViewSet(viewsets.ModelViewSet):
    """ViewSet for the asset class"""

    queryset = models.Asset.objects.all()
    serializer_class = serializers.AssetSerializer
    permission_classes = [permissions.IsAuthenticated]


class Asset_typeViewSet(viewsets.ModelViewSet):
    """ViewSet for the asset_type class"""

    queryset = models.Asset_type.objects.all()
    serializer_class = serializers.Asset_typeSerializer
    permission_classes = [permissions.IsAuthenticated]


class BrandViewSet(viewsets.ModelViewSet):
    """ViewSet for the loan_asset class"""

    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    permission_classes = [permissions.IsAuthenticated]


class LocationsViewSet(viewsets.ModelViewSet):
    """ViewSet for the locations class"""

    queryset = models.Locations.objects.all()
    serializer_class = serializers.LocationsSerializer
    permission_classes = [permissions.IsAuthenticated]


class Loan_assetViewSet(viewsets.ModelViewSet):
    """ViewSet for the loan_asset class"""

    queryset = models.Loan_asset.objects.all()
    serializer_class = serializers.Loan_assetSerializer
    permission_classes = [permissions.IsAuthenticated]


class Loaner_typeViewSet(viewsets.ModelViewSet):
    """ViewSet for the loaner_type class"""

    queryset = models.Loaner_type.objects.all()
    serializer_class = serializers.Loaner_typeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ModelViewSet(viewsets.ModelViewSet):
    """ViewSet for the model class"""

    queryset = models.Model.objects.all()
    serializer_class = serializers.ModelSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomViewSet(viewsets.ModelViewSet):
    """ViewSet for the room class"""

    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class Room_typeViewSet(viewsets.ModelViewSet):
    """ViewSet for the asset_type class"""

    queryset = models.Room_type.objects.all()
    serializer_class = serializers.Asset_typeSerializer
    permission_classes = [permissions.IsAuthenticated]


