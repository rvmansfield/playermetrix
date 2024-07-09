from django.contrib import admin
from players.models import Players, Events, Details, Blog



class playersAdmin(admin.ModelAdmin):
    search_fields = ['firstName', 'lastName']



# Register your models here.
admin.site.register(Players, playersAdmin)
admin.site.register(Events)
admin.site.register(Details)
admin.site.register(Blog)

