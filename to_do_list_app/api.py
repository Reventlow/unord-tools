from rest_framework import viewsets, permissions

from . import serializers
from . import models

class JobsViewSet(viewsets.ModelViewSet):
    """ViewSet for the Asset class"""

    queryset = models.Jobs.objects.all()
    serializer_class = serializers.JobsSerializer
    permission_classes = [permissions.IsAuthenticated]