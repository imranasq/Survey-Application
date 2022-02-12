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

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ["text"]

class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        options = kwargs.pop("options")
        choices = {(option.pk, option.text) for option in options}
        super().__init__(*args, **kwargs)
        option_field = forms.ChoiceField(choices=choices, widget=forms.RadioSelect, required=True)
        self.fields["option"] = option_field