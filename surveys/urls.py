from unicodedata import name
from django.urls import path
from .views import SurveyListView, SurveyCreateView, question_create

urlpatterns = [
    path("surveys/", SurveyListView.as_view(), name="survey-list"),
    path("surveys/create/",SurveyCreateView.as_view(), name="create-survey" ),
    path("surveys/<int:pk>/question/", question_create, name="survey-question-create"),
]