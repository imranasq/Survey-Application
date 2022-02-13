from django.urls import path
from .views import SurveyListView, SurveyCreateView, edit_survey, delete_survey, question_create, option_create, start_survey, active_survey_list, survey_report, survey_response

urlpatterns = [
    path("surveys/", SurveyListView.as_view(), name="survey_list"),
    path("surveys/create/",SurveyCreateView.as_view(), name="create_survey" ),
    path("surveys/<int:pk>/edit/", edit_survey, name="survey_edit"),
    path("surveys/<int:pk>/delete/", delete_survey, name="survey_delete"),
    path("surveys/<int:pk>/question/", question_create, name="survey_question_create"),
    path("surveys/<int:survey_pk>/question/<int:question_pk>/option/",option_create, name="survey_option_create"),
    path("surveys-list/", active_survey_list, name="active_survey"),
    path("surveys/<int:pk>/start/", start_survey, name="survey_start"),
    path("surveys/<int:pk>/", survey_report, name="survey_report"),
    path("surveys/<int:survey_pk>/response/<int:response_pk>", survey_response, name="survey_response"),
]