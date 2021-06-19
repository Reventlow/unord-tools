from django.db import models
from django.contrib.auth.models import User

class Jobs(models.Model):
    # Relationships

    # Fields
    item = models.CharField(max_length=200)
    to_do_owner =models.CharField(max_length=200, blank=True, null=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.item +' | ' +  str(self.completed)

