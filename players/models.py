from django.db import models


class Players(models.Model):
  firstName = models.CharField(max_length=255,default=None, blank=True)
  lastName = models.CharField(max_length=255,default=None, blank=True)
  highSchool = models.CharField(max_length=255,default=None, blank=True)
  gradYear = models.IntegerField(default=None, blank=True)
  throws = models.CharField(max_length=5,default=None, blank=True)
  hits = models.CharField(max_length=5,default=None, blank=True)
  image = models.BooleanField(default=0)
  picture = models.ImageField(default='default.jpg', upload_to='profile_images')
  instagramUser = models.CharField(max_length=255,default=None, blank=True)
  xUser = models.CharField(max_length=255,default=None, blank=True)
  slug = models.SlugField(default="", blank=True)
  pitcher = models.BooleanField(default=False)
  catcher = models.BooleanField(default=False)
  firstbase = models.BooleanField(default=False)
  secondbase = models.BooleanField(default=False)
  thirdbase = models.BooleanField(default=False)
  shortstop = models.BooleanField(default=False)
  leftfield = models.BooleanField(default=False)
  centerfield = models.BooleanField(default=False)
  rightfield = models.BooleanField(default=False)

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
  registration = models.BooleanField(default=True)

  def __str__(self):
      return f"{self.title} - {self.date}"

  class Meta:
      verbose_name_plural = "Events"

class Details(models.Model):
  event = models.ForeignKey(Events, on_delete=models.CASCADE)
  player = models.ForeignKey(Players, on_delete=models.CASCADE)
  height = models.IntegerField(default=None, blank=True, null=True)
  weight = models.IntegerField(default=None, blank=True, null=True)
  ifVelo = models.IntegerField(default=None, blank=True, null=True)
  ofVelo = models.IntegerField(default=None, blank=True, null=True)
  cVelo = models.IntegerField(default=None, blank=True, null=True)
  popTime = models.DecimalField(max_digits = 4,decimal_places = 2,default=None, blank=True, null=True)
  exitVelo = models.IntegerField(default=None, blank=True, null=True)
  sixtyyard = models.DecimalField(max_digits = 4,decimal_places = 2,default=None, blank=True, null=True)
  maxFB = models.IntegerField(default=None, blank=True, null=True)
  changeUp = models.IntegerField(default=None, blank=True, null=True)
  curve = models.IntegerField(default=None, blank=True, null=True)

  def __str__(self):
      return f"{self.player} / {self.event}"

  class Meta:
      verbose_name_plural = "Details"

class Blog(models.Model):
  title = models.CharField(max_length=255)
  date = models.DateField()
  details = models.TextField(default=None, blank=True)
  slug = models.SlugField(null=True)

  def __str__(self):
      return f"{self.title} - {self.date}"

  class Meta:
      verbose_name_plural = "Blog"


