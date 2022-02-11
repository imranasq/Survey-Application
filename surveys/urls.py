from django.urls import path
from .views import survey_list

urlpatterns = [
    path("surveys/", survey_list, name="survey-list"),
]