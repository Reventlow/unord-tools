from django.db import models
from django.contrib.auth.models import User

class Jobs(models.Model):
    # Relationships
    to_do_owner = models.ForeignKey("auth.User", on_delete=models.SET_NULL, blank=True, null=True)

    # Fields
    item = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.item +' | ' +  str(self.completed)

