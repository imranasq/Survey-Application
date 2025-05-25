from django.views import View
from django.views.generic import (
    ListView, CreateView, DeleteView
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.formsets import formset_factory
from django.db import transaction

from .models import Survey, Question, Answer, Response
from .forms import SurveyForm, QuestionForm, OptionForm, AnswerForm, BaseAnswerFormSet

# Survey List
class SurveyListView(LoginRequiredMixin, ListView):
    model = Survey
    template_name = "survey/survey-list.html"
    login_url = '/login/'

    def get_queryset(self):
        surveys = Survey.objects.filter(creator=self.request.user)
        return surveys
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['surveys'] = context['survey_list']
        return context

# Survey Create
class SurveyCreateView(LoginRequiredMixin, CreateView):
    form_class = SurveyForm
    template_name = "survey/create-survey.html"
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("survey_edit", kwargs={"pk": self.object.pk})

# Survey Edit
class SurveyEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        survey = get_object_or_404(Survey.objects.prefetch_related("question_set__option_set"), pk=pk, creator=request.user)
        questions = survey.question_set.all()
        return render(request, "survey/edit-survey.html", {"survey": survey, "questions": questions})

    def post(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk, creator=request.user)
        survey.is_active = True
        survey.save()
        return redirect("survey_list")

# Survey Delete
class SurveyDeleteView(LoginRequiredMixin, DeleteView):
    model = Survey
    template_name = "survey/survey_confirm_delete.html"  # Add this template
    success_url = reverse_lazy("survey_list")
    login_url = '/login/'

    def get_queryset(self):
        return self.model.objects.filter(creator=self.request.user)

# Question Create
class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = QuestionForm
    template_name = "survey/create-survey-question.html"
    login_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        self.survey = get_object_or_404(Survey, pk=kwargs['pk'], creator=request.user)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.survey = self.survey
        self.object = form.save()
        return redirect("survey_option_create", survey_pk=self.survey.pk, question_pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["survey"] = self.survey
        return context

# Option Create
class OptionCreateView(LoginRequiredMixin, View):
    def get(self, request, survey_pk, question_pk):
        survey = get_object_or_404(Survey, pk=survey_pk, creator=request.user)
        question = get_object_or_404(Question, pk=question_pk)
        form = OptionForm()
        return render(request, "survey/create-options.html", {
            "survey": survey,
            "question": question,
            "options": question.option_set.all(),
            "form": form
        })

    def post(self, request, survey_pk, question_pk):
        survey = get_object_or_404(Survey, pk=survey_pk, creator=request.user)
        question = get_object_or_404(Question, pk=question_pk)
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question = question
            option.save()
        return redirect("survey_option_create", survey_pk=survey_pk, question_pk=question_pk)

# Active Survey List
class ActiveSurveyListView(LoginRequiredMixin, ListView):
    model = Survey
    template_name = "survey/active-survey-list.html"
    login_url = '/login/'

    def get_queryset(self):
        return Survey.objects.filter(is_active=True).exclude(response_by=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['surveys'] = context['survey_list']
        return context

# Start Survey View
class StartSurveyView(LoginRequiredMixin, View):
    def get(self, request, pk):
        survey = get_object_or_404(
            Survey.objects.prefetch_related("question_set__option_set"), 
            pk=pk, 
            is_active=True
        )
        questions = survey.question_set.all()
        return render(request, "survey/start-survey.html", {
            "survey": survey,
            "questions": questions
        })

    def post(self, request, pk):
        survey = get_object_or_404(Survey, pk=pk, is_active=True)
        response = Response.objects.create(survey=survey)
        return redirect("survey_response", survey_pk=pk, response_pk=response.pk)


# Survey Report View
class SurveyReportView(LoginRequiredMixin, View):
    def get(self, request, pk):
        survey = get_object_or_404(Survey.objects.prefetch_related("question_set__option_set"), pk=pk, creator=request.user, is_active=True)
        questions = survey.question_set.all()
        for question in questions:
            option_pks = question.option_set.values_list("pk", flat=True)
            total_answers = Answer.objects.filter(option_id__in=option_pks).count()
            for option in question.option_set.all():
                num_answers = Answer.objects.filter(option=option).count()
                option.percent = 100.0 * num_answers / total_answers if total_answers else 0
        responses = survey.response_set.filter(is_complete=True).count()
        return render(request, "survey/survey-report.html", {
            "survey": survey,
            "questions": questions,
            "responses": responses
        })

# Survey Response View
class SurveyResponseView(LoginRequiredMixin, View):
    def get(self, request, survey_pk, response_pk):
        return self._render_form(request, survey_pk, response_pk)

    def post(self, request, survey_pk, response_pk):
        survey = get_object_or_404(Survey.objects.prefetch_related("question_set__option_set"), pk=survey_pk, is_active=True)
        response = get_object_or_404(Response, pk=response_pk, is_complete=False, survey=survey)

        questions = survey.question_set.all()
        options = [question.option_set.all() for question in questions]
        form_kwargs = {"empty_permitted": False, "options": options}
        AnswerFormSet = formset_factory(AnswerForm, extra=len(questions), formset=BaseAnswerFormSet)

        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)
        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    Answer.objects.create(
                        option_id=form.cleaned_data["option"],
                        response_id=response_pk,
                    )
                response.is_complete = True
                response.save()
            survey.response_by = request.user
            survey.save()
            return redirect("active_survey")
        return self._render_form(request, survey_pk, response_pk, formset)

    def _render_form(self, request, survey_pk, response_pk, formset=None):
        survey = get_object_or_404(Survey.objects.prefetch_related("question_set__option_set"), pk=survey_pk, is_active=True)
        response = get_object_or_404(Response, pk=response_pk, is_complete=False, survey=survey)

        questions = survey.question_set.all()
        options = [question.option_set.all() for question in questions]
        form_kwargs = {"empty_permitted": False, "options": options}
        AnswerFormSet = formset_factory(AnswerForm, extra=len(questions), formset=BaseAnswerFormSet)

        formset = formset or AnswerFormSet(form_kwargs=form_kwargs)
        question_forms = zip(questions, formset)
        return render(request, "survey/survey-response.html", {
            "survey": survey,
            "question_forms": question_forms,
            "formset": formset
        })
