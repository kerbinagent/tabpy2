from django.shortcuts import render
from feedback.forms import judge_form, tournament_form
from tournament.models import Tournament_Settings
from django.http import HttpResponseRedirect, HttpResponse

def judge_feedback(request):
    tournament_name = Tournament_Settings.objects.all()[0].Name_of_Tournament
    if request.method == "POST":
        form = judge_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return (HttpResponseRedirect('/feedback/feedback-success'))
        else:
            form = form
    else:
        form = judge_form()
    context_dict = {'tournament_name':tournament_name}
    context_dict['form']=form
    return render(request,'feedback.html',context_dict)

def feedback_tournament(request):
    tournament_name = Tournament_Settings.objects.all()[0].Name_of_Tournament
    if request.method == "POST":
        form = tournament_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return (HttpResponseRedirect('/feedback/feedback-success'))
        else:
            form = form
    else:
        form = tournament_form()
    context_dict = {'tournament_name':tournament_name}
    context_dict['form']=form
    return render(request,'feedback_tournament.html',context_dict)

def feedback_complete(request):
    tournament_name = Tournament_Settings.objects.all()[0].Name_of_Tournament
    context_dict = {'tournament_name':tournament_name}
    return render(request,'feedback_complete.html',context_dict)
