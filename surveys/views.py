from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from .models import Survey, Question
from django.http import Http404
from .forms import SurveyForm, QuestionForm, OptionForm
from django.views.generic import ListView, CreateView

# Create your views here.
class SurveyListView(ListView):
    model = Survey
    template_name = "survey/survey-list.html"

    def get_context_data(self, **kwargs):
        filtered_survey = Survey.objects.filter(creator=self.request.user.id)
        if filtered_survey.exists():
            surveys = filtered_survey
            context = {
                'surveys': surveys
            }
            return context


class SurveyCreateView(CreateView):
    template_name = "survey/create-survey.html"
    form_class = SurveyForm


    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.is_active=True
        return super(SurveyCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('survey-edit', kwargs={'pk': self.object.pk})

@login_required
def edit_survey(request, pk):
    try:
        survey = Survey.objects.prefetch_related("question_set__option_set").get(pk=pk, creator=request.user)
    except Survey.DoesNotExist:
        raise Http404()

    if request.method == "POST":
        survey.is_active = True
        survey.save()
        return redirect("survey-list")
    else:
        questions = survey.question_set.all()
        context={
            "survey": survey,
            "questions": questions
        }
        return render(request, "survey/edit-survey.html", context)

@login_required
def delete_survey(request, pk):
    survey = get_object_or_404(Survey, pk=pk, creator=request.user)
    if request.method == "POST":
        survey.delete()

    return redirect("survey-list")

# class QuestionCreateView(CreateView):
#     template_name = "survey/survey-question.html"
#     form_class = QuestionForm
#     success_url = reverse_lazy("survey-list")

#return redirect("survey-edit", pk=survey.id)
#     def form_valid(self, form):
#         survey = get_object_or_404(Survey, pk=self.kwargs['pk'], creator=self.request.user)
#         print("---------------------------",survey)
#         form.instance.servey=survey
#         print(form.instance.servey)
#         return super(SurveyCreateView, self).form_valid(form)

@login_required
def question_create(request, pk):
    survey = get_object_or_404(Survey, pk=pk, creator=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            return redirect("survey-option-create", survey_pk=pk, question_pk=question.pk)
    else:
        form = QuestionForm()

    context={
        "survey": survey,
        "form": form
    }

    return render(request, "survey/create-survey-question.html", context)

@login_required
def option_create(request, survey_pk, question_pk):
    survey = get_object_or_404(Survey, pk=survey_pk, creator=request.user)
    question = Question.objects.get(pk=question_pk)
    if request.method == "POST":
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question_id = question_pk
            option.save()
    else:
        form = OptionForm()

    options = question.option_set.all()
    context = {
        "survey": survey,
        "question": question,
        "options": options,
        "form": form
    }
    return render(request, "survey/create-options.html", context)