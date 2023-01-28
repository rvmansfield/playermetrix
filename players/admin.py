from django.contrib import admin
from players.models import Players, Events, Details

# Register your models here.
admin.site.register(Players)
admin.site.register(Events)
admin.site.register(Details)