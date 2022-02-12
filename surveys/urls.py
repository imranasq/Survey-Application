from django.urls import path
from .views import SurveyListView, SurveyCreateView, edit_survey, delete_survey, question_create, option_create, start_survey, active_survey_list

urlpatterns = [
    path("surveys/", SurveyListView.as_view(), name="survey-list"),
    path("surveys/create/",SurveyCreateView.as_view(), name="create-survey" ),
    path("surveys/<int:pk>/edit/", edit_survey, name="survey-edit"),
    path("surveys/<int:pk>/delete/", delete_survey, name="survey-delete"),
    path("surveys/<int:pk>/question/", question_create, name="survey-question-create"),
    path("surveys/<int:survey_pk>/question/<int:question_pk>/option/",option_create, name="survey-option-create"),
    path("surveys_list/", active_survey_list, name="active-survey"),
    path("surveys/<int:pk>/start/", start_survey, name="survey-start"),
]