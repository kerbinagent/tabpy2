from django.shortcuts import render
from tournament.models import School, Team, Speaker, Tournament_Settings
from registration.forms import team_form, speaker_form
from django.http import HttpResponse

def index(request):
    tournament_name = Tournament_Settings.objects.all()[0].Name_of_Tournament
    if request.method == "POST":
        form = team_form(request.POST)
        sform = speaker_form(request.POST)
        if form.is_valid() and sform.is_valid():
            #Create New Team
            form.save(commit=True)
            team_name = form.cleaned_data['name']
            team = Team.objects.get(name=team_name)
            #Create New Debater
            speaker_id = Speaker.objects.order_by('-speaker_id')[0].speaker_id
            sdata = sform.cleaned_data
            speaker = Speaker.objects.get_or_create(name=sdata['name1'],school=sdata['school1'],team=team,speaker_id=speaker_id+1,novice=sdata['novice1'])
            speaker = speaker[0]
            speaker.save()

            speaker = Speaker.objects.get_or_create(name=sdata['name2'],school=sdata['school2'],team=team,speaker_id=speaker_id+2,novice=sdata['novice2'])
            speaker = speaker[0]
            speaker.save()

            speaker = Speaker.objects.get_or_create(name=sdata['name3'],school=sdata['school3'],team=team,speaker_id=speaker_id+3,novice=sdata['novice3'])
            speaker = speaker[0]
            speaker.save()
        else:
            form = form
            sform = sform
    else:
        form = team_form()
        sform = speaker_form()

    context_dict={
    'form':form,
    'sform':sform,
    'tournament_name': tournament_name
    }
    return (render(request, 'registration.html',context_dict))
