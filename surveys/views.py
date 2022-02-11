from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Survey
from .forms import SurveyForm, QuestionForm
from django.views.generic import ListView, CreateView

# Create your views here.
class SurveyListView(ListView):
    model = Survey
    template_name = "survey-list.html"

    def get_context_data(self, **kwargs):
        filtered_survey = Survey.objects.filter(creator=self.request.user.id)
        if filtered_survey.exists():
            surveys = filtered_survey
        context = {
            'surveys': surveys
        }
        return context


class SurveyCreateView(CreateView):
    template_name = "create-survey.html"
    form_class = SurveyForm
    success_url = reverse_lazy("survey-list")


    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.is_active=True
        return super(SurveyCreateView, self).form_valid(form)

# class QuestionCreateView(CreateView):
#     template_name = "survey-question.html"
#     form_class = QuestionForm
#     success_url = reverse_lazy("survey-list")


#     def form_valid(self, form):
#         survey = get_object_or_404(Survey, pk=self.kwargs['pk'], creator=self.request.user)
#         print("---------------------------",survey)
#         form.instance.servey=survey
#         print(form.instance.servey)
#         return super(SurveyCreateView, self).form_valid(form)

@login_required
def question_create(request, pk):
    """User can add a question to a draft survey"""
    survey = get_object_or_404(Survey, pk=pk, creator=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect("survey-list")
    else:
        form = QuestionForm()

    return render(request, "survey-question.html", {"survey": survey, "form": form})

