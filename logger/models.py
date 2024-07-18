from django.db import models

# Create your models here.
class Log(models.Model):
  student = models.ForeignKey('base.Student', on_delete=models.CASCADE)
  user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
  subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
  time_spent = models.DecimalField(decimal_places=1, max_digits=10)
  hour_type = models.CharField(max_length=255)
  discription = models.CharField(max_length=255)
  date = models.DateField()


class Subject(models.Model):
  name = models.CharField(max_length=255)
  type = models.CharField(max_length=255, choices=[('Core', 'Core'), ('Elective', 'Elective')])
  user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

  def __str__(self):
    return self.name
  
class RequiredSubjects(models.Model):
  name = models.CharField(max_length=255)
  type = models.CharField(max_length=255, choices=[('Core', 'Core'), ('Elective', 'Elective')])
  state = models.ForeignKey('base.StateRequirements', on_delete=models.CASCADE)

  def __str__(self):
    return self.name
    
  