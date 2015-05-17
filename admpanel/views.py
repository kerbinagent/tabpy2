from django.shortcuts import render
from admpanel.forms import UserForm, VeriForm, BallotForm, SettingForm, MatchForm, JudgeForm, SchoolForm, RoomForm
from tournament.models import School, Judge, Speaker, Team, Room, Room_Stat, Tournament_Settings
from admpanel.models import Ballot, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

# Pick title name
def pick_name():
    s_count = Tournament_Settings.objects.count()
    if not s_count:
        return "Tournament Not Initiated"
    else:
        return Tournament_Settings.objects.all()[0].Name_of_Tournament


def check_init():
    # Error 1: No Setting, Error 2: No school, Error 3: Judge not enough; Error 4: Room Not Enough, Error 5: Odd Team Numbers
    error_list = []
    t_count = Team.objects.count()
    need_r = t_count // 2
    r_count = Room.objects.count()
    j_count = Judge.objects.count()
    s_count = Tournament_Settings.objects.count()
    sc_count = School.objects.count()
    if s_count == 0:
        error_list.append(1)
    if sc_count == 0:
        error_list.append(2)
    if j_count == 0 or j_count<need_r or j_count<r_count:
        error_list.append(3)
    if r_count < need_r:
        error_list.append(4)
    if t_count % 2 != 0:
        error_list.append(5)
    return error_list


def register(request):
    title_name = pick_name()
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        vericode = VeriForm(request.POST)

        adm_code = Tournament_Settings.objects.all()[0].Admin_Code
        jud_code = Tournament_Settings.objects.all()[0].Judge_Code
        if user_form.is_valid() and vericode.is_valid():
            # Register User
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Assign User Profile
            input_code = vericode.cleaned_data['veri_code'] == jud_code
            if input_code:
                judge = vericode.cleaned_data['judge']
                current_profile = UserProfile.objects.create(user = user, judge=judge, user_admin = False)
            else:
                current_profile = UserProfile.objects.create(user = user, judge=None, user_admin = True)
            current_profile.save()
            registered = True

    else:
        user_form = UserForm()
        vericode = VeriForm()
    context_dict = {'tournament_name':title_name, 'user_form': user_form, 'veri_form': vericode, 'registered': registered}
    return render(request,'register.html',context_dict)

def user_login(request):
    title_name = pick_name()
    error_message = False
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request, user)
                return (HttpResponseRedirect('/tournament'))
            else:
                error_message = "Sorry your account is disabled. Contact Technical Support"
        else:
            error_message = "Login failed. Username/Password Incorrect"
        context_dict = {'tournament_name':title_name,'error':error_message}
        return render(request,"login.html",context_dict)
    else:
        context_dict = {'tournament_name':title_name,'error':error_message}
        return render(request,"login.html",context_dict)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/tournament')

@login_required
def initpanel(request):
    # Detect Usertype (admin/judge/superuser)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.user_admin:
            return HttpResponseRedirect('/tournament/')
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/admin/')

    title_name = pick_name()
    context_dict = {'tournament_name':title_name}

    # Get Errorlist
    errorlist = check_init()
    error_type = [False,False,False,False,False]
    for error in errorlist:
        error_type[error-1] = True

    #Get Judge, Room, School list
    j_count = Judge.objects.count()
    if j_count == 0:
        judge_list = []
    else:
        judge_list = Judge.objects.all()
    r_count = Room.objects.count()
    if r_count == 0:
        room_list = []
    else:
        room_list = Room.objects.all()
    s_count = School.objects.count()
    if s_count == 0:
        school_list = []
    else:
        school_list = School.objects.all()
    context_dict['judge_list'] = judge_list
    context_dict['room_list'] = room_list
    context_dict['school_list'] = school_list

    #Start Setting
    if request.method == "POST":
        form = SettingForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        if 1 in errorlist:
            form = SettingForm
        else:
            form = ""
    context_dict['form'] = form
    context_dict['error_type'] = error_type
    return render(request,"init_panel.html",context_dict)

@login_required
def new_entry(request,new_type):
    # Detect User
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.user_admin:
            return HttpResponseRedirect('/tournament/')
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/admin/')

    title_name = pick_name()
    context_dict = {'tournament_name':title_name}

    # 1 is judge, 2 is room, 3 is school
    if new_type == "1":
        head_message = "New Judge"
    elif new_type == "2":
        head_message = "New Room"
    elif new_type == "3":
        head_message = "New School"
    else:
        head_message = ""
    context_dict['heading'] = head_message

    # Get forms needed
    form = ""
    if request.method == "POST":
        if new_type == "1":
            form = JudgeForm(request.POST)
        elif new_type == "2":
            form = RoomForm(request.POST)
        elif new_type == "3":
            form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admpanel/init')
    else:
        if new_type == "1":
            form = JudgeForm
        elif new_type == "2":
            form = RoomForm
        elif new_type == "3":
            form = SchoolForm
    context_dict['form'] = form
    return render(request,'new_entry.html',context_dict)


@login_required
def admpanel(request):
    # Detect Usertype (admin/judge/superuser)
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.user_admin:
            return HttpResponseRedirect('/tournament/')
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/admin/')

    # Add some message
    notice_list = []
    current_setting = Tournament_Settings.objects.all()[0]
    if current_setting.Registration_Open:
        notice_list.append("Registration Still Open (Cannot Proceed to Matchup)")
    else:
        team_number = Team.objects.count()
        notice_list.append("We have a total of "+str(team_number)+" teams")
        if team_number % 2 != 0:
            notice_list.append("You Don't have even number of teams. Remember to add a swing team")

    title_name = Tournament_Settings.objects.all()[0].Name_of_Tournament
    context_dict = {'tournament_name':title_name}
    # Getting all the ballots for presentation in ballot management
    if Ballot.objects.count() > 0:
        n = Ballot.objects.order_by('-round_number')[0].round_number
        ballot_list = []
        for i in range(1,n+1):
            duple = [i]
            filtered_ballots = Ballot.objects.filter(round_number=i)
            duple.append(filtered_ballots)
            ballot_list.append(duple)
        context_dict['ballots'] = ballot_list
    # Checking missing ballots from judge
    n = Ballot.objects.order_by('-round_number')[0].round_number
    n_r = Room_Stat.objects.order_by('-round_number')[0].round_number
    current_list = Ballot.objects.filter(round_number = n)
    flag = True
    judge_list = []
    for each_ballot in current_list:
        if each_ballot.p1s == 0:
            flag = False
            judge_list.append(each_ballot.judge)
    if flag:
        judge_list = None
    if n_r == 0:
        judge_list = None
        #Add the message that the admin should start initiating
        notice_list.append("Ready to Initiate Tournament. Close registration and go to judge tab to start Round 1")
    context_dict['notice_list'] = notice_list
    context_dict['missing_list'] = judge_list
    context_dict['generated'] = n != n_r
    context_dict['round_number'] = n_r

    # Edit matchup and Generate Ballots
    all_match = Room_Stat.objects.filter(round_number=n_r)
    context_dict['match_list'] = all_match

    # Check Matchup error
    error_message=[]
    all_judge = Judge.objects.all()
    for judge in all_judge:
        one_list = Room_Stat.objects.filter(chair = judge, round_number = n_r)
        if len(one_list) > 1:
            error_message.append("Judge Duplicate for "+judge.name)
    all_room = Room.objects.all()
    for room in all_room:
        one_list = Room_Stat.objects.filter(room_id = room, round_number = n_r)
        if len(one_list) > 1:
            error_message.append("ATTENTION! Room Duplicate for "+room.name)
    all_team = Team.objects.all()
    for team in all_team:
        one_list_p = Room_Stat.objects.filter(prop_team=team, round_number = n_r)
        one_list_o = Room_Stat.objects.filter(oppo_team=team, round_number = n_r)
        if len(one_list_p)+len(one_list_o) > 1:
            error_message.append("Team Duplicate for "+team.name)
    context_dict['error_message'] = error_message

    # Edit Settings
    if request.method == "POST":
        form = SettingForm(request.POST, instance = current_setting)
        if form.is_valid():
            form.save()
            return (HttpResponseRedirect('/admpanel/'))
    else:
        form = SettingForm(instance = current_setting)
    context_dict['form'] = form

    return render(request,'admpanel.html',context_dict)

@login_required
def ballot_edit(request,ballot_id):
    error_message = None
    n = Room_Stat.objects.order_by('-round_number')[0].round_number
    ballot_id = int(ballot_id)
    title_name = Tournament_Settings.objects.all()[0].Name_of_Tournament
    context_dict = {'tournament_name':title_name}
    current_ballot = Ballot.objects.get(ballot_id=ballot_id)
    outdated = False
    if current_ballot.round_number != n:
        outdated = True
    # Detect User
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.user_admin:
            current_judge = user_profile.judge
            if current_judge != current_ballot.judge:
                error_message = "This is not your ballot"
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/admin/')

    context_dict['error'] = error_message
    context_dict['outdated'] = outdated
    # Fetch Ballot
    if request.method == "POST":
        form = BallotForm(request.POST, instance = current_ballot)
        if form.is_valid():
            form.save()
            return (HttpResponseRedirect('/admpanel/'))
    else:
        form = BallotForm(instance=current_ballot)
    context_dict['form'] = form
    context_dict['current_ballot'] = current_ballot
    return render(request,'ballot_edit.html',context_dict)

@login_required
def matchup_edit(request,matchup_id):
    error_message = None
    n = Room_Stat.objects.order_by('-round_number')[0].round_number
    matchup_id = int(matchup_id)
    title_name = Tournament_Settings.objects.all()[0].Name_of_Tournament
    context_dict = {'tournament_name':title_name}
    current_match = Room_Stat.objects.get(matchup_id = matchup_id)
    if current_match.round_number != n:
        error_message = "Past Matchups Cannot be Edited"
    # Detect User Type
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.user_admin:
            error_message = "Only Admin is allowed to edit matchups"
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect('/admin/')
    # Fetch matchup
    if request.method == "POST":
        form = MatchForm(request.POST, instance = current_match)
        if form.is_valid():
            form.save()
            return (HttpResponseRedirect('/admpanel/'))
    else:
        form = MatchForm(instance = current_match)
    context_dict['form'] = form
    context_dict['current_match'] = current_match
    context_dict['error_message'] = error_message
    return (render(request,'match_edit.html',context_dict))
