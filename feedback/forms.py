from django import forms
from feedback.models import judge_feedback, tournament_feedback
from tournament.models import Judge


class judge_form(forms.ModelForm):
    judge = forms.ModelChoiceField(queryset=Judge.objects.all(), help_text="Judge")
    fair_score = forms.IntegerField(min_value = 1,max_value=5, help_text="Rate how fair the judge is ranging from 1-5")
    clarity_score = forms.IntegerField(min_value = 1,max_value=5, help_text="Rate how clear the judge is during feedback from 1-5")
    friendly_score = forms.IntegerField(min_value = 1,max_value=5, help_text="Rate how friendly the judge is during the tournament from 1-5")
    knowledge_score = forms.IntegerField(min_value = 1,max_value=5, help_text="Rate how knowledgeble the judge is from 1-5")
    availability_score = forms.IntegerField(min_value = 1,max_value=5, help_text="Rate how accessible the judge is througout the tournament form 1-5")
    feedback_text = forms.CharField(required=False, widget=forms.Textarea, help_text="Please provide any additional information you would want us to know")

    class Meta:
        model = judge_feedback
        fields = ('judge','fair_score','clarity_score','friendly_score','knowledge_score','availability_score','feedback_text')

class tournament_form(forms.ModelForm):
    motion_score = forms.IntegerField(min_value=1, max_value=5, help_text="Rate the quality of the motions from 1-5")
    adjudication_score = forms.IntegerField(min_value=1, max_value=5, help_text="Rate the quality of adjudication from 1-5")
    competitive_score = forms.IntegerField(min_value=1, max_value=5, help_text="Rate the level of competitiveness from 1-5")
    food_score = forms.IntegerField(min_value=1, max_value=5, help_text="Rate the quality and quantity of food from 1-5")
    accomodation_score = forms.IntegerField(min_value=1, max_value=5, help_text="Rate the comfortness of accomodation from 1-5")
    transportation_score = forms.IntegerField(min_value=1, max_value=5, help_text="Rate the convenience of transportation from 1-5")
    affordability_score = forms.IntegerField(min_value=1, max_value=5, help_text="Rate the affordability from 1-5")
    overall_score = forms.IntegerField(min_value=1, max_value=5, help_text="Rate the overall quality of the tournament from 1-5")
    feedback_text = forms.CharField(required=False, widget=forms.Textarea, help_text="Please provide any additional information you would want us to know")

    class Meta:
        model = tournament_feedback
        fields = ('motion_score','adjudication_score','competitive_score','food_score','accomodation_score','transportation_score','affordability_score','overall_score','feedback_text')
