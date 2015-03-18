from django import forms
from django.forms import ValidationError
from tournament.models import School, Team, Speaker

def team_validator(name):
    teams = Team.objects.filter(name=name)
    if teams:
        raise ValidationError('Team Already Exist')

def number_validator(number):
    numbers = Team.objects.filter(contact_number=number)
    if numbers:
        raise ValidationError('Number Already Exist')

def email_validator(email):
    emails = Team.objects.filter(contact_email=email)
    if emails:
        raise ValidationError('Email Already Exist')


class team_form(forms.ModelForm):
    name = forms.CharField(max_length=64,help_text="Team Name",validators=[team_validator])
    school = forms.ModelChoiceField(queryset=School.objects.all(),help_text="School")
    contact_person = forms.CharField(max_length=32,help_text="Contact Person")
    contact_number = forms.IntegerField(help_text="Contact Phone",validators=[number_validator])
    contact_email = forms.EmailField(help_text="Contact Email",validators=[email_validator])
    novice = forms.BooleanField(help_text="Check if team is novice", initial=False, required=False)

    class Meta:
        model = Team
        fields = ('name','school','contact_person','contact_number','contact_email','novice')

class speaker_form(forms.Form):
    name1 = forms.CharField(max_length=64, help_text="Debater 1 Name")
    school1 = forms.ModelChoiceField(queryset=School.objects.all(),help_text="School")
    novice1 = forms.BooleanField(help_text="Check if this debater is novice", initial=False, required=False)

    name2 = forms.CharField(max_length=64, help_text="Debater 2 Name")
    school2 = forms.ModelChoiceField(queryset=School.objects.all(),help_text="School")
    novice2 = forms.BooleanField(help_text="Check if this debater is novice", initial=False, required=False)

    name3 = forms.CharField(max_length=64, help_text="Debater 3 Name")
    school3 = forms.ModelChoiceField(queryset=School.objects.all(),help_text="School")
    novice3 = forms.BooleanField(help_text="Check if this debater is novice", initial=False, required=False)
