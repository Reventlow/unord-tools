from rest_framework import viewsets, permissions

from . import serializers
from . import models


class AssetViewSet(viewsets.ModelViewSet):
    """ViewSet for the Asset class"""

    queryset = models.Asset.objects.all()
    serializer_class = serializers.AssetSerializer
    permission_classes = [permissions.IsAuthenticated]


class Asset_typeViewSet(viewsets.ModelViewSet):
    """ViewSet for the Asset_type class"""

    queryset = models.Asset_type.objects.all()
    serializer_class = serializers.Asset_typeSerializer
    permission_classes = [permissions.IsAuthenticated]


class BrandViewSet(viewsets.ModelViewSet):
    """ViewSet for the Brand class"""

    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    permission_classes = [permissions.IsAuthenticated]

class Bundle_reservationViewSet(viewsets.ModelViewSet):
    """ViewSet for the Bundle_reservation class"""

    queryset = models.Brand.objects.all()
    serializer_class = serializers.Bundle_reservationSerializer
    permission_classes = [permissions.IsAuthenticated]


class LocationsViewSet(viewsets.ModelViewSet):
    """ViewSet for the Locations class"""

    queryset = models.Locations.objects.all()
    serializer_class = serializers.LocationsSerializer
    permission_classes = [permissions.IsAuthenticated]


class Loan_assetViewSet(viewsets.ModelViewSet):
    """ViewSet for the Loan_asset class"""

    queryset = models.Loan_asset.objects.all()
    serializer_class = serializers.Loan_assetSerializer
    permission_classes = [permissions.IsAuthenticated]


class Loaner_typeViewSet(viewsets.ModelViewSet):
    """ViewSet for the Loaner_type class"""

    queryset = models.Loaner_type.objects.all()
    serializer_class = serializers.Loaner_typeSerializer
    permission_classes = [permissions.IsAuthenticated]


class Model_hardwareViewSet(viewsets.ModelViewSet):
    """ViewSet for the Model class"""

    queryset = models.Model_hardware.objects.all()
    serializer_class = serializers.Model_hardwareSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoomViewSet(viewsets.ModelViewSet):
    """ViewSet for the Room class"""

    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class Room_typeViewSet(viewsets.ModelViewSet):
    """ViewSet for the Room_type class"""

    queryset = models.Room_type.objects.all()
    serializer_class = serializers.Room_typeSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoutinesViewSet(viewsets.ModelViewSet):
    """ViewSet for the Routines class"""

    queryset = models.Routines.objects.all()
    serializer_class = serializers.RoutinesSerializer
    permission_classes = [permissions.IsAuthenticated]


class RoutineLogViewSet(viewsets.ModelViewSet):
    """ViewSet for the RoutineLog class"""

    queryset = models.RoutineLog.objects.all()
    serializer_class = serializers.RoutineLogSerializer
    permission_classes = [permissions.IsAuthenticated]


