import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tabpy2.settings')

import django
django.setup()

from tournament.models import Team

team_list = Team.objects.order_by('-total_wl','-total_sp','-total_mg')
temp_list = []
for team in team_list:
    temp = []
    temp.append(team.name)
    temp.append(team.total_wl)
    temp_list.append(temp)
print (temp_list)
print (temp_list[0][0])
