from rest_framework import viewsets, permissions

from . import serializers
from . import models


class locationsViewSet(viewsets.ModelViewSet):
    """ViewSet for the locations class"""

    queryset = models.Locations.objects.all()
    serializer_class = serializers.locationsSerializer
    permission_classes = [permissions.IsAuthenticated]


class asset_typeViewSet(viewsets.ModelViewSet):
    """ViewSet for the asset_type class"""

    queryset = models.Asset_type.objects.all()
    serializer_class = serializers.asset_typeSerializer
    permission_classes = [permissions.IsAuthenticated]


class loan_assetViewSet(viewsets.ModelViewSet):
    """ViewSet for the loan_asset class"""

    queryset = models.Loan_asset.objects.all()
    serializer_class = serializers.loan_assetSerializer
    permission_classes = [permissions.IsAuthenticated]


class roomViewSet(viewsets.ModelViewSet):
    """ViewSet for the room class"""

    queryset = models.Room.objects.all()
    serializer_class = serializers.roomSerializer
    permission_classes = [permissions.IsAuthenticated]


class assetViewSet(viewsets.ModelViewSet):
    """ViewSet for the asset class"""

    queryset = models.Asset.objects.all()
    serializer_class = serializers.assetSerializer
    permission_classes = [permissions.IsAuthenticated]


class loaner_typeViewSet(viewsets.ModelViewSet):
    """ViewSet for the loaner_type class"""

    queryset = models.Loaner_type.objects.all()
    serializer_class = serializers.loaner_typeSerializer
    permission_classes = [permissions.IsAuthenticated]


class modelViewSet(viewsets.ModelViewSet):
    """ViewSet for the model class"""

    queryset = models.Model.objects.all()
    serializer_class = serializers.modelSerializer
    permission_classes = [permissions.IsAuthenticated]
