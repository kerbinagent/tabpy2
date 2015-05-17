import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tabpy2.settings')
import hashlib
import django
django.setup()

from tournament.models import Team, Speaker, Judge


judges_all = Judge.objects.all()
for judge in judges_all:
    judge.round_filled = -1
    pwd = judge.name+"suonidafahao"
    pwd = hashlib.sha256(pwd.encode())
    pwd = pwd.hexdigest()
    pwd = pwd[:4]
    judge.code = pwd
    judge.save()
