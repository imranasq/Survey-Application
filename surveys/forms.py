from django import forms

from .models import Survey, Question, Option


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["title"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title"]