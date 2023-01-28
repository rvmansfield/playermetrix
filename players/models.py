from django.db import models

class Players(models.Model):
  firstName = models.CharField(max_length=255)
  lastName = models.CharField(max_length=255)
  highSchool = models.CharField(max_length=255)
  gradYear = models.IntegerField()
  throws = models.CharField(max_length=5)
  hits = models.CharField(max_length=5)
  slug = models.SlugField(default="", null=False)

  def __str__(self):
      return f"{self.firstName} {self.lastName}"

  class Meta:
      verbose_name_plural = "Players"


class Events(models.Model):
  title = models.CharField(max_length=255)
  location = models.CharField(max_length=255)
  date = models.DateField()
  eventDetails = models.TextField(default=None, blank=True)
  link = models.CharField(max_length=100,default=None, blank=True)

  def __str__(self):
      return f"{self.title} - {self.date}"

  class Meta:
      verbose_name_plural = "Events"

class Details(models.Model):
  event = models.ForeignKey(Events, on_delete=models.CASCADE)
  player = models.ForeignKey(Players, on_delete=models.CASCADE)
  height = models.IntegerField(default=None, blank=True)
  weight = models.IntegerField(default=None, blank=True)
  ifVelo = models.IntegerField(default=None, blank=True)
  ofVelo = models.IntegerField(default=None, blank=True)
  cVelo = models.IntegerField(default=None, blank=True)
  popTime = models.DecimalField(max_digits = 4,decimal_places = 2,default=None, blank=True)
  exitVelo = models.IntegerField(default=None, blank=True)
  sixtyyard = models.DecimalField(max_digits = 4,decimal_places = 2,default=None, blank=True)
  maxFB = models.IntegerField(default=None, blank=True)
  changeUp = models.IntegerField(default=None, blank=True)
  curve = models.IntegerField(default=None, blank=True)

  def __str__(self):
      return f"{self.player} / {self.event}"

  class Meta:
      verbose_name_plural = "Details"

