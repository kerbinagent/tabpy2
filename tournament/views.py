from django.shortcuts import render
from tournament.models import Judge, Room_Stat, Speaker, Team, SpeakerPoint, Room, Tournament_Settings
from tournament.forms import CodeForm, JudgeBallot, AdminForm
from django.http import HttpResponseRedirect, HttpResponse

#Check for duplicate ballots
def check_duplicate():
    n = SpeakerPoint.objects.order_by('-round_number')[0]
    n = n.round_number
    n = SpeakerPoint.objects.filter(round_number=n)
    speaker_n = Speaker.objects.count()
    if len(n) == speaker_n:
        flag = True
    else:
        flag = False
    flag2 = False
    teams_all = Team.objects.all()
    std_postr = len(teams_all[0].po_str)
    for team in teams_all:
        if len(team.po_str) != std_postr:
            flag2 = True
    return (flag and flag2)

#Judge code input
def index(request):
    if check_duplicate():
        return (HttpResponse('Fatal Error! Duplicate Ballots, report to your admin immediately'))
    initiate = Room_Stat.objects.get_or_create(round_number=0, prop_team=Team.objects.all()[0],oppo_team=Team.objects.all()[1], chair=Judge.objects.all()[0],room_id=Room.objects.all()[0])
    n = Room_Stat.objects.order_by('-round_number')[0]
    break_number = Tournament_Settings.objects.all()[0].Total_Rounds
    registration_open = Tournament_Settings.objects.all()[0].Registration_Open
    #Ininiate first matchup
    n = n.round_number
    if n==0 and (not registration_open):
        return (HttpResponseRedirect('/tournament/initiate_matchup'))
    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            redirect = '/tournament/judge/'+form.cleaned_data['code']
            return HttpResponseRedirect(redirect)
        else:
            context_dict={'form':form}
    else:
        form = CodeForm()
    team_all = Team.objects.all()
    flag = True
    for team in team_all:
        if len(team.po_str) != n:
            flag = False
    context_dict = {'form':form}
    context_dict['n'] = str(n)
    context_dict['break_status'] = (n == break_number) and flag
    context_dict['tournament_name'] = Tournament_Settings.objects.all()[0].Name_of_Tournament
    context_dict['tab_released'] = Tournament_Settings.objects.all()[0].Tab_Released
    return (render(request,'index.html',context_dict))

#Ballot for Judge
def judge(request,judge_code):
    if check_duplicate():
        return (HttpResponse('Fatal Error! Duplicate Ballots, report to your admin immediately'))
    #Get Judge name
    tournament_name = Tournament_Settings.objects.all()[0].Name_of_Tournament
    try:
        judge=Judge.objects.get(code=judge_code)
    except Judge.DoesNotExist:
        judge=None
    if judge:
        context_dict={'judge_name':judge.name}
    else:
        context_dict={'judge_name':None}
    n = Room_Stat.objects.order_by('-round_number')[0]
    n = n.round_number
    context_dict['round_number']=str(n)
    context_dict['tournament_name']=tournament_name
    #Get Match-up Data to display
    if judge:
        try:
            round_match = Room_Stat.objects.get(chair=judge.name, round_number=n)
            if judge.round_filled == n:
                return (HttpResponseRedirect('/tournament/'))
        except Room_Stat.DoesNotExist:
            context_dict['judge_name'] = None
            round_match = None
    else:
        round_match = None
    if round_match:
        prop_team = Team.objects.get(name=round_match.prop_team)
        oppo_team = Team.objects.get(name=round_match.oppo_team)
        context_dict['prop_team'] = prop_team.name
        context_dict['oppo_team'] = oppo_team.name
        prop_speakers = Speaker.objects.filter(team=prop_team)
        p1 = prop_speakers[0]
        p2 = prop_speakers[1]
        p3 = prop_speakers[2]
        oppo_speakers = Speaker.objects.filter(team=oppo_team)
        o1 = oppo_speakers[0]
        o2 = oppo_speakers[1]
        o3 = oppo_speakers[2]
        context_dict['p1']=p1
        context_dict['p2']=p2
        context_dict['p3']=p3
        context_dict['o1']=o1
        context_dict['o2']=o2
        context_dict['o3']=o3
    context_dict['round_check'] = round_match
    #Save Ballot data
    if request.method == "POST":
        form = JudgeBallot(request.POST)
        if form.is_valid():
            #Team Score
            prop_sum = form.cleaned_data['prop_1']+form.cleaned_data['prop_2']+form.cleaned_data['prop_3']+form.cleaned_data['prop_reply']
            oppo_sum = form.cleaned_data['oppo_1']+form.cleaned_data['oppo_2']+form.cleaned_data['oppo_3']+form.cleaned_data['oppo_reply']
            split = form.cleaned_data['split']
            if prop_sum > oppo_sum:
                prop_team.total_wl +=1
                if split:
                    prop_team.total_ballots += 2
                    oppo_team.total_ballots += 1
                else:
                    prop_team.total_ballots += 3
            else:
                oppo_team.total_wl +=1
                if split:
                    oppo_team.total_ballots += 2
                    prop_team.total_ballots += 1
                else:
                    oppo_team.total_ballots += 3

            prop_team.total_po +=1
            prop_team.total_sp += prop_sum
            oppo_team.total_sp += oppo_sum
            prop_team.total_mg += prop_sum-oppo_sum
            oppo_team.total_mg += oppo_sum-prop_sum
            prop_team.po_str = prop_team.po_str + "1"
            oppo_team.po_str = oppo_team.po_str + "0"
            prop_team.save()
            oppo_team.save()
            #Individual Score
            p1.total_sp += form.cleaned_data['prop_1']
            point_object = SpeakerPoint.objects.get_or_create(speaker_id=p1, round_number=n)[0]
            point_object.point = form.cleaned_data['prop_1']
            point_object.save()
            p1.save()

            p2.total_sp += form.cleaned_data['prop_2']
            point_object = SpeakerPoint.objects.get_or_create(speaker_id=p2, round_number=n)[0]
            point_object.point = form.cleaned_data['prop_2']
            point_object.save()
            p2.save()

            p3.total_sp += form.cleaned_data['prop_3']
            point_object = SpeakerPoint.objects.get_or_create(speaker_id=p3, round_number=n)[0]
            point_object.point = form.cleaned_data['prop_3']
            point_object.save()
            p3.save()

            o1.total_sp += form.cleaned_data['oppo_1']
            point_object = SpeakerPoint.objects.get_or_create(speaker_id=o1, round_number=n)[0]
            point_object.point = form.cleaned_data['oppo_1']
            point_object.save()
            o1.save()

            o2.total_sp += form.cleaned_data['oppo_2']
            point_object = SpeakerPoint.objects.get_or_create(speaker_id=o2, round_number=n)[0]
            point_object.point = form.cleaned_data['oppo_2']
            point_object.save()
            o2.save()

            o3.total_sp += form.cleaned_data['oppo_3']
            point_object = SpeakerPoint.objects.get_or_create(speaker_id=o3, round_number=n)[0]
            point_object.point = form.cleaned_data['oppo_3']
            point_object.save()
            o3.save()

            judge.round_filled = n
            judge.save()

            #Detect Need to Matchup
            if len(SpeakerPoint.objects.filter(round_number=n)) == Speaker.objects.count():
                return (HttpResponseRedirect('/tournament/initiate_matchup'))
            else:
                return (HttpResponseRedirect('/tournament/'))
        else:
            context_dict['form'] = form
    else:
        context_dict['form'] = JudgeBallot()
    return (render(request,'judge.html',context_dict))

#Match Up
def matchup(request):
    registration_open = Tournament_Settings.objects.all()[0].Registration_Open
    if registration_open:
        return (HttpResponseRedirect('/tournament/'))
    if check_duplicate():
        return (HttpResponse('Fatal Error! Duplicate Ballots, report to your admin immediately'))
    initiate = Room_Stat.objects.get_or_create(round_number=0, prop_team=Team.objects.all()[0],oppo_team=Team.objects.all()[1], chair=Judge.objects.all()[0],room_id=Room.objects.all()[0])
    n = Room_Stat.objects.order_by('-round_number')[0]
    n_int = n.round_number
    n = float(n.round_number)
    break_rounds = Tournament_Settings.objects.all()[0].Total_Rounds
    if n_int == break_rounds:
        return (HttpResponseRedirect('/tournament/'))
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
        room_stat = Room_Stat.objects.get_or_create(round_number=n_int+1, chair=judge_list[i], prop_team=pair_list[i][0], oppo_team=pair_list[i][1], room_id=room_list[i])[0]
        room_stat.save()
        i+=1
    return (HttpResponseRedirect('/tournament/'))

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

def judge_check(request):
    if check_duplicate():
        return (HttpResponse('Fatal Error! Duplicate Ballots, report to your admin immediately'))
    context_dict = {}
    n = Room_Stat.objects.order_by('-round_number')[0]
    n = n.round_number
    break_number = Tournament_Settings.objects.all()[0].Total_Rounds
    team_all = Team.objects.all()
    flag = True
    for team in team_all:
        if len(team.po_str) != n:
            flag = False
    break_status = (n == break_number) and flag
    #If Breaking available
    if break_status:
        if request.method == "POST":
            form = AdminForm(request.POST)
            if form.is_valid():
                admin_code = form.cleaned_data['code']
                return (HttpResponseRedirect('/tournament/breaking/'+admin_code))
            else:
                context_dict = {'form':form}
        else:
            form = AdminForm()
        context_dict['break_status'] = break_status
        context_dict['form'] = form
    #If breaking not available
    try:
        judge_list = Judge.objects.filter(round_filled=n-1)
    except Judge.DoesNotExist:
        judge_list = None
    if n == 1:
        judge_list = Judge.objects.filter(round_filled=-1)
    tournament_name = Tournament_Settings.objects.all()[0].Name_of_Tournament
    context_dict['judge_list'] = judge_list
    context_dict['round_number'] = n
    context_dict['tournament_name'] = tournament_name
    context_dict['break_status'] = break_status
    return (render(request,'judge_check.html',context_dict))

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
