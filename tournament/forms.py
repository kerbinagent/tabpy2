from django import forms

class CodeForm(forms.Form):
    code = forms.CharField(max_length=8, label='Input your assigned Judge Code')

class JudgeBallot(forms.Form):
    prop_1 = forms.IntegerField()
    prop_2 = forms.IntegerField()
    prop_3 = forms.IntegerField()
    prop_reply = forms.FloatField()
    oppo_1 = forms.IntegerField()
    oppo_2 = forms.IntegerField()
    oppo_3 = forms.IntegerField()
    oppo_reply = forms.FloatField()
