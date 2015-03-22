from django.contrib import admin
from feedback.models import judge_feedback, tournament_feedback

class JudgeAdmin(admin.ModelAdmin):
    list_display = ("judge","fair_score","clarity_score","friendly_score")

admin.site.register(judge_feedback, JudgeAdmin)
admin.site.register(tournament_feedback)
