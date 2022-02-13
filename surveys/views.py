from cmath import log
from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from .models import Response, Survey, Question, Answer
from django.http import Http404
from .forms import SurveyForm, QuestionForm, OptionForm, AnswerForm, BaseAnswerFormSet
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.forms.formsets import formset_factory

# Create your views here.
class SurveyListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
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


class SurveyCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = "survey/create-survey.html"
    form_class = SurveyForm


    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(SurveyCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('survey_edit', kwargs={'pk': self.object.pk})

@login_required
def edit_survey(request, pk):
    survey = Survey.objects.prefetch_related("question_set__option_set").get(pk=pk, creator=request.user)
    if request.method == "POST":
        survey.is_active = True
        survey.save()
        return redirect("survey_list")
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

    return redirect("survey_list")

# class QuestionCreateView(CreateView):
#     template_name = "survey/survey-question.html"
#     form_class = QuestionForm
#     success_url = reverse_lazy("survey_list")

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
            return redirect("survey_option_create", survey_pk=pk, question_pk=question.pk)
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

@login_required
def active_survey_list(request):
    surveys = Survey.objects.filter(is_active=True).exclude(response_by = request.user)
    context={
        "surveys": surveys
    }
    return render(request, "survey/active-survey-list.html", context)

@login_required
def start_survey(request, pk):
    survey = get_object_or_404(Survey, pk=pk, is_active=True)
    if request.method == "POST":
        response = Response.objects.create(survey=survey)
        return redirect("survey_response", survey_pk=pk, response_pk = response.pk)
    context={
        "survey": survey
    }
    return render(request, "survey/start-survey.html", context)

@login_required
def survey_report(request, pk):
    survey = Survey.objects.prefetch_related("question_set__option_set").get(pk=pk, creator=request.user, is_active=True)
    questions = survey.question_set.all()

    for question in questions:
        option_pks = question.option_set.values_list("pk", flat=True)
        total_answers = Answer.objects.filter(option_id__in=option_pks).count()
        for option in question.option_set.all():
            num_answers = Answer.objects.filter(option=option).count()
            if total_answers:
                option.percent = 100.0 * num_answers / total_answers

            else:
                option.percent = 0

    responses = survey.response_set.filter(is_complete=True).count()
    context = {
        "survey": survey,
        "questions": questions,
        "responses": responses
    }
    return render(request, "survey/survey-report.html", context)

@login_required
def survey_response(request, survey_pk, response_pk):
    survey = Survey.objects.prefetch_related("question_set__option_set").get(pk=survey_pk, is_active=True)
    response = survey.response_set.get(pk=response_pk, is_complete=False)

    questions = survey.question_set.all()
    options = [question.option_set.all() for question in questions]
    form_kwargs = {"empty_permitted": False, "options": options}
    AnswerFormSet = formset_factory(AnswerForm, extra=len(questions), formset=BaseAnswerFormSet)
    if request.method == "POST":
        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)
        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    Answer.objects.create(
                        option_id=form.cleaned_data["option"], response_id=response_pk,
                    )

                response.is_complete = True
                response.save()
            survey.response_by = request.user
            survey.save()
            return redirect("active_survey")

    else:
        formset = AnswerFormSet(form_kwargs=form_kwargs)

    question_forms = zip(questions, formset)
    context={
        "survey": survey,
        "question_forms": question_forms,
        "formset": formset
    }
    return render(request, "survey/survey-response.html", context)