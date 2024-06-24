from django.db import models
from django.contrib.auth.models import User

class LogEntry(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    subject = models.CharField(max_length=255)
    hour_type = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='log_entries')
    dependents = models.ForeignKey('Dependents', on_delete=models.CASCADE, related_name='dependents')

    def __str__(self):
        return f"{self.subject} ({self.user.username}) from {self.start} to {self.end}"

class Dependents(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)