from django.urls import path

from .views import (
    SurveyListView,
    SurveyCreateView,
    SurveyEditView,
    SurveyDeleteView,
    QuestionCreateView,
    OptionCreateView,
    StartSurveyView,
    ActiveSurveyListView,
    SurveyReportView,
    SurveyResponseView,
)

urlpatterns = [
    path("surveys/", SurveyListView.as_view(), name="survey_list"),
    path("surveys/create/", SurveyCreateView.as_view(), name="create_survey"),
    path("surveys/<int:pk>/edit/", SurveyEditView.as_view(), name="survey_edit"),
    path("surveys/<int:pk>/delete/", SurveyDeleteView.as_view(), name="survey_delete"),
    path("surveys/<int:pk>/question/", QuestionCreateView.as_view(), name="survey_question_create"),
    path("surveys/<int:survey_pk>/question/<int:question_pk>/option/", OptionCreateView.as_view(), name="survey_option_create"),
    path("surveys-list/", ActiveSurveyListView.as_view(), name="active_survey"),
    path("surveys/<int:pk>/start/", StartSurveyView.as_view(), name="survey_start"),
    path("surveys/<int:pk>/", SurveyReportView.as_view(), name="survey_report"),
    path("surveys/<int:survey_pk>/response/<int:response_pk>", SurveyResponseView.as_view(), name="survey_response"),
]
