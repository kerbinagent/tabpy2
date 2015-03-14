import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tabpy2.settings')

import django
django.setup()

from tournament.models import School,Team,Speaker,Judge,Room

def add_school(name):
    school = School.objects.get_or_create(name=name)[0]
    school.save()
    return school

def add_Team(name, school):
    t = Team.objects.get_or_create(name=name, school=school)[0]
    t.save()
    return t

def add_Speaker(name, team, school, numberid):
    s = Speaker.objects.get_or_create(name=name, team=team, school=school, speaker_id=numberid)[0]
    s.save()
    return s

def add_Room(name):
    r = Room.objects.get_or_create(name=name)[0]
    r.save()
    return r

def add_judge(name):
    j = Judge.objects.get_or_create(name=name)[0]
    j.save()
    return j

add_school('open')

school = School.objects.all()[0]

add_Team('test 1',school)

team1 = Team.objects.get(name='test 1')

add_Team('test 2',school)

team2 = Team.objects.get(name='test 2')

i=0

while i<3:
    speaker_name='Smart '+str(i)
    add_Speaker(speaker_name, team1, school, i)
    i+=1

i=3
while i<6:
    speaker_name='Dumb '+str(i)
    add_Speaker(speaker_name,team2,school,i)
    i+=1

add_judge('Water Judge')

add_Room('111')
