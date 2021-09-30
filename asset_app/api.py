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

class AssetCaseViewSet(viewsets.ModelViewSet):
    """ViewSet for the AssetCase class"""

    queryset = models.AssetCase.objects.all()
    serializer_class = serializers.AssetCaseSerializer
    permission_classes = [permissions.IsAuthenticated]

class AssetLogViewSet(viewsets.ModelViewSet):
    """ViewSet for the AssetLog class"""

    queryset = models.AssetLog.objects.all()
    serializer_class = serializers.AssetLogSerializer
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

class ExternalServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for the ExternalService class"""

    queryset = models.ExternalService.objects.all()
    serializer_class = serializers.ExternalServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExternalServiceContactViewSet(viewsets.ModelViewSet):
    """ViewSet for the ExternalServiceContact class"""

    queryset = models.ExternalServiceContact.objects.all()
    serializer_class = serializers.ExternalServiceContactSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExternalServicePositionViewSet(viewsets.ModelViewSet):
    """ViewSet for the ExternalServicePosition class"""

    queryset = models.ExternalServicePosition.objects.all()
    serializer_class = serializers.ExternalServicePositionSerializer
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


class One2OneInfoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Model class"""

    queryset = models.One2OneInfo.objects.all()
    serializer_class = serializers.One2OneInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class One2OneInfoLogViewSet(viewsets.ModelViewSet):
    """ViewSet for the Model class"""

    queryset = models.One2OneInfoLog.objects.all()
    serializer_class = serializers.One2OneInfoLogSerializer
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


class SeverityLevelViewSet(viewsets.ModelViewSet):
    """ViewSet for the SeverityLevel class"""

    queryset = models.SeverityLevel.objects.all()
    serializer_class = serializers.SeverityLevelSerializer
    permission_classes = [permissions.IsAuthenticated]

class SmsViewSet(viewsets.ModelViewSet):
    """ViewSet for the Sms class"""

    queryset = models.Sms.objects.all()
    serializer_class = serializers.SmsSerializer
    permission_classes = [permissions.IsAuthenticated]

class SmsLogViewSet(viewsets.ModelViewSet):
    """ViewSet for the SmsLog class"""

    queryset = models.SmsLog.objects.all()
    serializer_class = serializers.SmsLogSerializer
    permission_classes = [permissions.IsAuthenticated]


