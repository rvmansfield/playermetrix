from django.db import models
from django.contrib.auth.models import User
from players.models import Players


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    player = models.OneToOneField(Players, on_delete=models.CASCADE,blank=True,null=True)

    city = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=2,blank=True,null=True)
    
    

    def __str__(self):
        return self.user.username