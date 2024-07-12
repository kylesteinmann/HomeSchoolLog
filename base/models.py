from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    birthdate = models.CharField(max_length=255, blank=False, null=False)
    grade = models.CharField(max_length=255, blank=False, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class StateRequirements(models.Model):
    state = models.CharField(max_length=50, blank=False, null=True)
    core_hours = models.DecimalField(decimal_places=0, max_digits=10)
    total_hours = models.DecimalField(decimal_places=0, max_digits=10)
    year_start = models.DateField()
    year_end = models.DateField()

    def __str__(self):
        return self.state
    
class Profile(models.Model):
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    state = models.ForeignKey(StateRequirements, on_delete=models.CASCADE, related_name='profiles')
    email = models.EmailField()

    def __str__(self):
        return self.user.username
    
