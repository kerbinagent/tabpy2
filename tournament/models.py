from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return (self.name)

class Team(models.Model):
    name = models.CharField(max_length=64, unique=True)
    school = models.ForeignKey(School)
    contact_person = models.CharField(default="None",max_length=32)
    contact_number = models.IntegerField(default=10000)
    contact_email = models.EmailField(default="example@example.com")
    total_wl = models.IntegerField(default=0)
    total_po = models.IntegerField(default=0)
    total_ballots = models.IntegerField(default=0)
    po_str = models.CharField(max_length=32, default="", blank=True)
    total_sp = models.FloatField(default=0)
    total_mg = models.FloatField(default=0)
    novice = models.BooleanField(default=False)
    pull_up = models.BooleanField(default=False)
    slug = models.SlugField(max_length=128,unique=True)

    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        super(Team, self).save(*args, **kwargs)

    def __unicode__(self):
        return (self.name)

class Speaker(models.Model):
    team = models.ForeignKey(Team)
    school = models.ForeignKey(School)
    speaker_id = models.IntegerField(unique=True, default=0, primary_key=True)
    name = models.CharField(max_length=64)
    total_sp = models.IntegerField(default=0)
    novice = models.BooleanField(default=False)

    def __unicode__(self):
        return (str(self.speaker_id)+self.name)

class SpeakerPoint(models.Model):
    speaker_id = models.ForeignKey(Speaker)
    round_number = models.IntegerField(default=1)
    point = models.IntegerField(default=0)

    def __unicode__(self):
        return (self.speaker_id.name+' score for Round '+str(self.round_number))

class Judge(models.Model):
    name = models.CharField(max_length=64, unique=True, primary_key=True)
    code = models.CharField(max_length=8, unique=True, default='CODE')
    weight = models.IntegerField(default=1)
    round_filled = models.IntegerField(default=0)

    def __unicode__(self):
        return (self.name)

class Room(models.Model):
    name = models.CharField(max_length=64, unique=True)
    distance_to_hall = models.IntegerField(default=0)

    def __unicode__(self):
        return (self.name)

class Room_Stat(models.Model):
    prop_team = models.ForeignKey(Team,related_name='prop_team')
    oppo_team = models.ForeignKey(Team,related_name='oppo_team')
    room_id = models.ForeignKey(Room)
    chair = models.ForeignKey(Judge)
    panel1 = models.ForeignKey(Judge, related_name='panel1',null=True, blank=True)
    panel2 = models.ForeignKey(Judge, related_name='panel2',null=True, blank=True)
    round_number = models.IntegerField(default=1)

    def __unicode__(self):
        return ("Round "+str(self.round_number)+" in "+str(self.room_id))

class Tournament_Settings(models.Model):
    Name_of_Tournament = models.CharField(max_length=64, default="new tournament")
    Max_Margin = models.IntegerField(default=300)
    Score_Max = models.IntegerField(default=90)
    Score_Min = models.IntegerField(default=60)
    Total_Rounds = models.IntegerField(default=8)
    Novice_Breaks = models.IntegerField(default=4)
    Breaks = models.IntegerField(default=16)
    Tab_Released = models.BooleanField(default=False)
    Registration_Open = models.BooleanField(default=True)

    def __unicode__(self):
        return ("Global Setting for Tournament")
