from django.db import models

class Players(models.Model):
  firstName = models.CharField(max_length=255)
  lastName = models.CharField(max_length=255)
  highSchool = models.CharField(max_length=255)
  gradYear = models.IntegerField()
  throws = models.CharField(max_length=5)
  hits = models.CharField(max_length=5)

  def __str__(self):
      return f"{self.firstName} {self.lastName}"