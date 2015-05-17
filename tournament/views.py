from django.shortcuts import render
from tournament.models import Judge, Room_Stat, Speaker, Team, SpeakerPoint, Room, Tournament_Settings
from django.contrib.auth.decorators import login_required
from admpanel.views import check_init
from admpanel.models import Ballot, UserProfile
from tournament.forms import JudgeBallot, AdminForm
from django.http import HttpResponseRedirect, HttpResponse

#initiate matchup
def create_init():
    initiate = Room_Stat.objects.get_or_create(matchup_id = 0,round_number=0, prop_team=Team.objects.all()[0],oppo_team=Team.objects.all()[1], chair=Judge.objects.all()[0],room_id=Room.objects.all()[0])
    p_team = Team.objects.all()[0]
    o_team = Team.objects.all()[1]
    p_speakers = Speaker.objects.filter(team=p_team)
    o_speakers = Speaker.objects.filter(team=o_team)
    ballot_initiate = Ballot.objects.get_or_create(
    ballot_id = 0, judge = Judge.objects.all()[0], room = Room.objects.all()[0], p_team = p_team, o_team = o_team, round_number=0,
    p_1 = p_speakers[0], p_2 = p_speakers[1], p_3 = p_speakers[2],
    o_1 = o_speakers[0], o_2 = o_speakers[1], o_3 = o_speakers[2],split=False
    )

def ballot_creation(n):
    pair_list = Room_Stat.objects.filter(round_number=n)
    for pair in pair_list:
        base_n = Ballot.objects.order_by('-ballot_id')[0].ballot_id
        p_team = pair.prop_team
        p_speakers = Speaker.objects.filter(team=p_team)
        o_team = pair.oppo_team
        o_speakers = Speaker.objects.filter(team=o_team)
        new_ballot = Ballot.objects.get_or_create(
        ballot_id = base_n+1, judge = pair.chair, room = pair.room_id, p_team = p_team, o_team = o_team,round_number = n,
        p_1 = p_speakers[0], p_2 = p_speakers[1], p_3 = p_speakers[2],
        o_1 = o_speakers[0], o_2 = o_speakers[1], o_3 = o_speakers[2],split=False
        )[0]
        new_ballot.save()

#Check for duplicate ballots
def check_duplicate():
    return False

#Home
def index(request):
    if len(check_init()) != 0:
        return HttpResponseRedirect('/admpanel/init')
    t_setting = Tournament_Settings.objects.count()
    if t_setting == 0:
        return (HttpResponseRedirect('/admin/'))
    else:
        tm_count = Team.objects.count()
        if tm_count < 2:
            return (HttpResponseRedirect('/registration/'))
        else:
            create_init()
    if check_duplicate():
        return (HttpResponse('Fatal Error! Duplicate Ballots, report to your admin immediately'))
    create_init()
    n = Room_Stat.objects.order_by('-round_number')[0]
    break_number = Tournament_Settings.objects.all()[0].Total_Rounds
    registration_open = Tournament_Settings.objects.all()[0].Registration_Open
    n = n.round_number
    team_all = Team.objects.all()
    flag = True
    for team in team_all:
        if len(team.po_str) != n:
            flag = False
    context_dict = {'tournament_name':Tournament_Settings.objects.all()[0].Name_of_Tournament}
    context_dict['n'] = str(n)
    context_dict['break_status'] = (n == break_number) and flag
    context_dict['tab_released'] = Tournament_Settings.objects.all()[0].Tab_Released
    return (render(request,'index.html',context_dict))

#Ballot for Judge
@login_required
def judge(request):
    #Detect Usertype (admin/judge/superuser)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_admin:
            return HttpResponseRedirect('/admpanel/')
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/admin/')
    judge = user_profile.judge
    n = Ballot.objects.order_by('-round_number')[0].round_number
    try:
        judge_ballot = Ballot.objects.get(judge=judge, round_number=n)
    except Ballot.DoesNotExist:
        return HttpResponseRedirect('/tournament/')
    current_ballot_id = judge_ballot.ballot_id
    return HttpResponseRedirect('/admpanel/ballot/'+str(current_ballot_id))

def process_ballot(n):
    all_ballots = Ballot.objects.filter(round_number=n)
    for ballot in all_ballots:
        #Team Save
        p_team = ballot.p_team
        o_team = ballot.o_team
        p_sum = ballot.p1s+ballot.p2s+ballot.p3s+ballot.prs
        o_sum = ballot.o1s+ballot.o2s+ballot.o3s+ballot.ors
        if ballot.split:
            winner_ballot = 2
        else:
            winner_ballot = 3
        if p_sum == o_sum:
            return HttpResponse("Fatal Error! Ballot ID "+str(ballot.ballot_id)+" has no winner")
        p_team.total_po += 1
        p_team.po_str += '1'
        o_team.po_str += '0'
        p_team.total_sp += p_sum
        o_team.total_sp += o_sum
        p_team.total_mg += p_sum-o_sum
        o_team.total_mg += o_sum-p_sum
        if p_sum > o_sum:
            p_team.total_wl +=1
            p_team.total_ballots += winner_ballot
            o_team.total_ballots += 3-winner_ballot
        else:
            o_team.total_wl +=1
            o_team.total_ballots += winner_ballot
            p_team.total_ballots += 3-winner_ballot
        p_team.save()
        o_team.save()

        #Speaker Save
        p_1 = ballot.p_1
        p_1.total_sp += ballot.p1s
        p_2 = ballot.p_2
        p_2.total_sp += ballot.p2s
        p_3 = ballot.p_3
        p_3.total_sp += ballot.p3s
        o_1 = ballot.o_1
        o_1.total_sp += ballot.o1s
        o_2 = ballot.o_2
        o_2.total_sp += ballot.o2s
        o_3 = ballot.o_3
        o_3.total_sp += ballot.o3s
        p_1.save()
        p_2.save()
        p_3.save()
        o_1.save()
        o_2.save()
        o_3.save()

#Check if match_up has been generated
def matchup_check():
    n = Ballot.objects.order_by('-round_number')[0].round_number
    n_r = Room_Stat.objects.order_by('-round_number')[0].round_number
    if n == n_r:
        return False
    else:
        return True

@login_required
def matchup(request):
    #Detect Usertype (admin/judge/superuser)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.user_admin:
            return HttpResponseRedirect('/tournament/')
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/admin/')

    create_init()
    registration_open = Tournament_Settings.objects.all()[0].Registration_Open
    if registration_open:
        return (HttpResponseRedirect('/tournament/'))
    if check_duplicate():
        return (HttpResponse('Fatal Error! Duplicate Ballots, report to your admin immediately'))
    n = Room_Stat.objects.order_by('-round_number')[0]
    n_int = n.round_number
    n = float(n.round_number)
    break_rounds = Tournament_Settings.objects.all()[0].Total_Rounds
    if n_int == break_rounds:
        return (HttpResponseRedirect('/tournament/'))
    if matchup_check():
        return HttpResponse("Matchup already generated!")
    if n_int > 0:
        process_ballot(n_int)
    #Rank Team and Split into brackets
    ranked_list = Team.objects.order_by('-total_wl','-total_sp','-total_mg')
    bracket_list = []
    i=1
    j=0
    while i<len(ranked_list):
        if ranked_list[i].total_wl != ranked_list[i-1].total_wl:
            bracket_list.append(ranked_list[j:i])
            j=i
        i+=1
    bracket_list.append(ranked_list[j:])
    #Pull Up
    i=0
    while i<len(bracket_list)-1:
        if len(bracket_list[i]) % 2 == 0:
            i+=1
        else:
            j = len(bracket_list[i+1])-1
            k = 0
            while j>=0:
                if not bracket_list[i+1][j].pull_up:
                    k=j
                j-=1
            bracket_list[i].append(bracket_list[i+1][k])
            bracket_list[i+1][k].pull_up = True
            bracket_list[i+1][k].save()
            bracket_list[i+1] = bracket_list[i+1][:k]+bracket_list[i+1][k+1:]
    i=0
    while i<len(bracket_list):
        if bracket_list[i] == []:
            bracket_list = bracket_list[:i]+bracket_list[i+1:len(bracket_list)]
        i+=1
    #Build Pairings
    pair_list=[]
    i=0
    while i<len(bracket_list):
        k=len(bracket_list[i])-1
        j=0
        temppair=[]
        while j<(k+1)/2:
            temppair=[]
            temppair.append(bracket_list[i][j])
            temppair.append(bracket_list[i][k-j])
            pair_list.append(temppair)
            j+=1
        i+=1
    #Prop Oppo
    i=0
    while i<len(pair_list):
        flag = False
        if "111" in pair_list[i][0].po_str:
            flag = True
        if "000" in pair_list[i][1].po_str:
            flag = True
        if (pair_list[i][0].total_po > (n/2)) and (pair_list[i][1].total_po < (n/2)):
            flag = True
        if flag:
            temp = pair_list[i][0]
            pair_list[i][0] = pair_list[i][1]
            pair_list[i][1] = temp
        i+=1
    #Assigning Judge and Rooms
    judge_list = Judge.objects.order_by('-weight')
    room_list = Room.objects.order_by('distance_to_hall')
    i=0
    while i<len(pair_list):
        current_id = Room_Stat.objects.order_by('-matchup_id')[0].matchup_id
        room_stat = Room_Stat.objects.get_or_create(matchup_id = current_id+1, round_number=n_int+1, chair=judge_list[i], prop_team=pair_list[i][0], oppo_team=pair_list[i][1], room_id=room_list[i])[0]
        room_stat.save()
        i+=1
    print (n_int+1)
    return (HttpResponseRedirect('/admpanel/'))

#Create ballots
@login_required
def matchup_next(request,n):
    #Detect User type
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.user_admin:
            return HttpResponseRedirect('/tournament/')
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/admin/')
    n_int = int(n)
    ballot_creation(n)
    return HttpResponseRedirect("/admpanel/")

def show_tab(request):
    team_all = Team.objects.order_by('-total_wl','-total_sp','-total_mg')
    speaker_all = Speaker.objects.order_by('-total_sp')
    team_novice = Team.objects.filter(novice=True).order_by('-total_wl','-total_sp','-total_mg')
    speaker_novice = Speaker.objects.filter(novice=True).order_by('-total_sp')
    context_dict = {
    'team_all':team_all,
    'speaker_all':speaker_all,
    'team_novice':team_novice,
    'speaker_novice':speaker_novice}
    tournament_name = Tournament_Settings.objects.all()[0].Name_of_Tournament
    context_dict['tournament_name'] = tournament_name
    context_dict['Tab_Released'] = Tournament_Settings.objects.all()[0].Tab_Released

    return (render(request,'show_tab.html',context_dict))

def breaking(request, admin_code):
    settings = Tournament_Settings.objects.all()[0]
    correct_code = settings.Admin_Code
    breaks = settings.Breaks
    novice_breaks = settings.Novice_Breaks
    tournament_name = settings.Name_of_Tournament
    context_dict = {'valid_code':admin_code==correct_code}
    total_teams = Team.objects.order_by('-total_wl','-total_sp','-total_mg')
    if len(total_teams) >= breaks:
        breaking_list = total_teams[:breaks]
    else:
        breaking_list = None
    rest_list = total_teams[breaks:]
    novice_list = []
    if len(rest_list) >= novice_breaks:
        i=0
        while i< len(rest_list):
            if rest_list[i].novice:
                novice_list.append(rest_list[i])
            i+=1
        if len(novice_list) < novice_breaks:
            novice_list = None
        else:
            novice_list = novice_list[:novice_breaks]
    else:
        novice_list = None
    context_dict['tournament_name'] = tournament_name
    context_dict['novicebreak'] = novice_list
    context_dict['mainbreak'] = breaking_list
    return (render(request,'breaking.html',context_dict))

def show_matchup(request, round_number):
    registration_open = Tournament_Settings.objects.all()[0].Registration_Open
    if registration_open:
        return (HttpResponseRedirect('/tournament/'))
    if check_duplicate():
        return (HttpResponse('Fatal Error! Duplicate Ballots, report to your admin immediately'))
    try:
        room_stat = Room_Stat.objects.filter(round_number=int(round_number))
    except Room_Stat.DoesNotExist:
        room_stat = None
    context_dict = {'room_stat':room_stat}
    tournament_name = Tournament_Settings.objects.all()[0].Name_of_Tournament
    context_dict['tournament_name'] = tournament_name
    context_dict['round_number'] = room_stat[0].round_number
    return (render(request,'matchup.html',context_dict))
