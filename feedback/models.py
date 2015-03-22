from django.db import models
from tournament.models import Judge

class judge_feedback(models.Model):
    score_choice = (
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
    )
    judge = models.ForeignKey(Judge)
    fair_score = models.IntegerField(choices = score_choice)
    clarity_score = models.IntegerField(choices = score_choice)
    friendly_score = models.IntegerField(choices = score_choice)
    knowledge_score = models.IntegerField(choices = score_choice)
    availability_score = models.IntegerField(choices = score_choice)
    feedback_text = models.TextField(blank=True, null=True)

    def __unicode__(self):
        judge_name = self.judge.name
        return ('Feedback for '+judge_name)

class tournament_feedback(models.Model):
    score_choice = (
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
    )
    motion_score = models.IntegerField(choices = score_choice)
    adjudication_score = models.IntegerField(choices = score_choice)
    competitive_score = models.IntegerField(choices = score_choice)
    food_score = models.IntegerField(choices = score_choice)
    accomodation_score = models.IntegerField(choices = score_choice)
    transportation_score = models.IntegerField(choices = score_choice)
    affordability_score = models.IntegerField(choices = score_choice)
    overall_score = models.IntegerField(choices = score_choice)
    feedback_text = models.TextField(blank=True,null=True)
