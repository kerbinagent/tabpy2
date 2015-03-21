from django import forms
from tournament.models import Tournament_Settings, Judge, Room_Stat
from django.forms import ValidationError

def judgevalidator(code):
    try:
        judge = Judge.objects.get(code=code)
        n = Room_Stat.objects.order_by('-round_number')[0]
        n = n.round_number
        if judge.round_filled == n:
            raise ValidationError("You Have Already Turned in Ballot")
    except Judge.DoesNotExist:
        raise ValidationError("Judge Code Incorrect")
    if Tournament_Settings.objects.all()[0].Tab_Released:
        raise ValidationError("Tournament has ended")
    registration_open = Tournament_Settings.objects.all()[0].Registration_Open
    if registration_open:
        raise ValidationError("Tournament hasn't started (Registration still open)")

class CodeForm(forms.Form):
    code = forms.CharField(max_length=8, validators=[judgevalidator])

def adminvalidator(code):
    correct_code = Tournament_Settings.objects.all()[0].Admin_Code
    if code != correct_code:
        raise ValidationError("Admin Code Incorrect")

class AdminForm(forms.Form):
    code = forms.CharField(max_length=8, validators=[adminvalidator])

def scorevalidator(score):
    settings = Tournament_Settings.objects.all()[0]
    if score > settings.Score_Max or score < settings.Score_Min:
        raise ValidationError("Score out of range")

def replyvalidator(score):
    settings = Tournament_Settings.objects.all()[0]
    if score > settings.Score_Max/2 or score < score < settings.Score_Min/2:
        raise ValidationError("Reply Score out of range")

class JudgeBallot(forms.Form):
    winner_choice = (
    ('p','Proposition'),
    ('o','Opposition'),
    )
    prop_1 = forms.IntegerField(validators=[scorevalidator])
    prop_2 = forms.IntegerField(validators=[scorevalidator])
    prop_3 = forms.IntegerField(validators=[scorevalidator])
    prop_reply = forms.FloatField(validators=[replyvalidator])
    oppo_1 = forms.IntegerField(validators=[scorevalidator])
    oppo_2 = forms.IntegerField(validators=[scorevalidator])
    oppo_3 = forms.IntegerField(validators=[scorevalidator])
    oppo_reply = forms.FloatField(validators=[replyvalidator])
    winner = forms.ChoiceField(choices = winner_choice, required=True)
    split = forms.BooleanField(required=False, initial=False)

    def clean(self):
        form_data = self.cleaned_data
        margin_limit = Tournament_Settings.objects.all()[0]
        margin_limit = margin_limit.Max_Margin
        flag = True
        if not 'prop_1' in self.cleaned_data:
            flag = False
        if not 'prop_2' in self.cleaned_data:
            flag = False
        if not 'prop_3' in self.cleaned_data:
            flag = False
        if not 'oppo_1' in self.cleaned_data:
            flag = False
        if not 'oppo_2' in self.cleaned_data:
            flag = False
        if not 'oppo_3' in self.cleaned_data:
            flag = False
        if not 'prop_reply' in self.cleaned_data:
            flag = False
        if not 'oppo_reply' in self.cleaned_data:
            flag = False
        if flag:
            prop_sum = self.cleaned_data['prop_1']+self.cleaned_data['prop_2']+self.cleaned_data['prop_3']+self.cleaned_data['prop_reply']
            oppo_sum = self.cleaned_data['oppo_1']+self.cleaned_data['oppo_2']+self.cleaned_data['oppo_3']+self.cleaned_data['oppo_reply']
            if abs(prop_sum - oppo_sum) > margin_limit:
                raise ValidationError("Margin Out of Limit")
            if (prop_sum > oppo_sum and self.cleaned_data['winner'] == 'o') or (prop_sum < oppo_sum and self.cleaned_data['winner'] == 'p'):
                raise ValidationError("Winner has lower scores. Check your ballot again")
            if (prop_sum == oppo_sum):
                raise ValidationError("The score on prop and oppo is the same. You must choose a winner")
        return (self.cleaned_data)
