from rest_framework import serializers
from . import models

class JobsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Jobs
        fields = [
        "item",
        "to_do_owner",
        "completed",
        "last_updated",
        "created",
        ]