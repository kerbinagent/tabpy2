from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from tournament.models import Tournament_Settings, Judge, Room_Stat, School, Room
from admpanel.models import Ballot, UserProfile

def scorevalidator(score):
    settings = Tournament_Settings.objects.all()[0]
    if score > settings.Score_Max or score < settings.Score_Min:
        raise ValidationError("Score out of range")

def replyvalidator(score):
    settings = Tournament_Settings.objects.all()[0]
    if score > settings.Score_Max/2 or score < settings.Score_Min/2:
        raise ValidationError("Reply Score out of range")

def veri_validator(code):
    adm_code = Tournament_Settings.objects.all()[0].Admin_Code
    jud_code = Tournament_Settings.objects.all()[0].Judge_Code
    if (code != adm_code) and (code != jud_code):
        raise ValidationError('registration code incorrect')

def judge_validator(judge):
    try:
        UserProfile.objects.get(judge=judge)
        raise ValidationError('Judge already registered!')
    except UserProfile.DoesNotExist:
        flag = False

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','password','email')

class JudgeForm(forms.ModelForm):

    class Meta:
        model = Judge

class RoomForm(forms.ModelForm):

    class Meta:
        model = Room

class SchoolForm(forms.ModelForm):

    class Meta:
        model = School

class VeriForm(forms.Form):
    judge = forms.ModelChoiceField(queryset=Judge.objects.all(), required=False, validators=[judge_validator])
    veri_code = forms.CharField(max_length=8, validators=[veri_validator])

    def clean(self):
        jud_code = Tournament_Settings.objects.all()[0].Judge_Code
        flag = True
        if not 'judge' in self.cleaned_data:
            flag = False
        if not 'veri_code' in self.cleaned_data:
            flag = False
        if flag:
            if (self.cleaned_data['veri_code'] == jud_code) and self.cleaned_data['judge'] == None:
                raise ValidationError('Please select who are you')

class SettingForm(forms.ModelForm):

    class Meta:
        model = Tournament_Settings

class MatchForm(forms.ModelForm):

    class Meta:
        model = Room_Stat
        fields = ('prop_team','oppo_team','chair','room_id')

class BallotForm(forms.ModelForm):
    winner_choice = (
    ('p','Proposition'),
    ('o','Opposition'),
    )
    p1s = forms.IntegerField(validators=[scorevalidator])
    p2s = forms.IntegerField(validators=[scorevalidator])
    p3s = forms.IntegerField(validators=[scorevalidator])
    o1s = forms.IntegerField(validators=[scorevalidator])
    o2s = forms.IntegerField(validators=[scorevalidator])
    o3s = forms.IntegerField(validators=[scorevalidator])
    prs = forms.FloatField(validators=[replyvalidator])
    ors = forms.FloatField(validators=[replyvalidator])
    split = forms.BooleanField(required = False)
    winner = forms.ChoiceField(choices = winner_choice, required=True)

    def clean(self):
        margin_limit = Tournament_Settings.objects.all()[0]
        margin_limit = margin_limit.Max_Margin
        flag = True
        if not 'p1s' in self.cleaned_data:
            flag = False
        if not 'p2s' in self.cleaned_data:
            flag = False
        if not 'p3s' in self.cleaned_data:
            flag = False
        if not 'o1s' in self.cleaned_data:
            flag = False
        if not 'o2s' in self.cleaned_data:
            flag = False
        if not 'o3s' in self.cleaned_data:
            flag = False
        if not 'prs' in self.cleaned_data:
            flag = False
        if not 'ors' in self.cleaned_data:
            flag = False
        if flag:
            prop_sum = self.cleaned_data['p1s']+self.cleaned_data['p2s']+self.cleaned_data['p3s']+self.cleaned_data['prs']
            oppo_sum = self.cleaned_data['o1s']+self.cleaned_data['o2s']+self.cleaned_data['o3s']+self.cleaned_data['ors']
            if abs(prop_sum - oppo_sum) > margin_limit:
                raise ValidationError("Margin Out of Limit")
            if (prop_sum > oppo_sum and self.cleaned_data['winner'] == 'o') or (prop_sum < oppo_sum and self.cleaned_data['winner'] == 'p'):
                raise ValidationError("Winner has lower scores. Check your ballot again")
            if (prop_sum == oppo_sum):
                raise ValidationError("The score on prop and oppo is the same. You must choose a winner")
        return (self.cleaned_data)


    class Meta:
        model = Ballot
        fields = ('p1s','p2s','p3s','o1s','o2s','o3s','prs','ors','split')
