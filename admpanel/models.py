from django.db import models
from django.contrib.auth.models import User
from tournament.models import Judge, Team, Room, Speaker, Tournament_Settings

# Create your models here.
class Ballot(models.Model):
    ballot_id = models.IntegerField(unique=True, default = 0)
    judge = models.ForeignKey(Judge,related_name="judge")
    p_team = models.ForeignKey(Team,related_name="p_team")
    o_team = models.ForeignKey(Team,related_name="o_team")
    room = models.ForeignKey(Room,related_name="room")
    round_number = models.IntegerField(default = -1)
    p_1 = models.ForeignKey(Speaker,related_name="p_1")
    p1s = models.IntegerField(default = 0)
    p_2 = models.ForeignKey(Speaker,related_name="p_2")
    p2s = models.IntegerField(default = 0)
    p_3 = models.ForeignKey(Speaker,related_name="p_3")
    p3s = models.IntegerField(default = 0)
    o_1 = models.ForeignKey(Speaker,related_name="o_1")
    o1s = models.IntegerField(default = 0)
    o_2 = models.ForeignKey(Speaker,related_name="o_2")
    o2s = models.IntegerField(default = 0)
    o_3 = models.ForeignKey(Speaker,related_name="o_3")
    o3s = models.IntegerField(default = 0)
    prs = models.FloatField(default = 0)
    ors = models.FloatField(default = 0)
    split = models.BooleanField(default = False)

    def __unicode__(self):
        return ("Ballots from "+self.judge.name+" in round "+str(self.round_number))

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    judge = models.OneToOneField(Judge, blank=True, null=True)
    user_admin = models.BooleanField(default = False)

    def __unicode__(self):
        return ("User Profile for user "+self.user.username)
