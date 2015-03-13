from django.contrib import admin
from tournament.models import School,Team,Speaker,SpeakerPoint,Judge,Room,Room_Stat

class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(School)
admin.site.register(Team,TeamAdmin)
admin.site.register(Speaker)
admin.site.register(SpeakerPoint)
admin.site.register(Judge)
admin.site.register(Room)
admin.site.register(Room_Stat)
