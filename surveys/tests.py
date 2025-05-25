import pytest
from django.urls import reverse
from .models import Survey, Question, Option, Response

from django.contrib.auth import get_user_model

User = get_user_model() 

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", email="testuser@example.com", password="#1Testpass")

@pytest.fixture
def authenticated_client(client, user):
    logged_in = client.login(username="testuser", password="#1Testpass")
    assert logged_in, "Login failed in fixture!"
    return client

@pytest.fixture
def survey(user):
    return Survey.objects.create(title="Test Survey", creator=user)

@pytest.fixture
def question(survey):
    return Question.objects.create(text="Sample Question", survey=survey)

@pytest.fixture
def option(question):
    return Option.objects.create(text="Option 1", question=question)


def test_survey_list_view_redirects_for_anonymous(client):
    response = client.get(reverse("survey_list"))
    assert response.status_code == 302
    assert "/login/" in response.url


def test_survey_list_view(authenticated_client):
    response = authenticated_client.get(reverse("survey_list"))
    assert response.status_code == 200


# def test_survey_create_view(authenticated_client):
#     response = authenticated_client.post(reverse("create_survey"), {"title": "New Survey"})
#     assert response.status_code == 302  # Redirect after success


# def test_survey_edit_view(authenticated_client, survey):
#     response = authenticated_client.get(reverse("survey_edit", args=[survey.pk]))
#     assert response.status_code == 200


# def test_survey_delete_view(authenticated_client, survey):
#     response = authenticated_client.post(reverse("survey_delete", args=[survey.pk]))
#     assert response.status_code == 302
#     assert not Survey.objects.filter(pk=survey.pk).exists()


# def test_question_create_view(authenticated_client, survey):
#     url = reverse("survey_question_create", args=[survey.pk])
#     response = authenticated_client.post(url, {"text": "What is your name?"})
#     assert response.status_code == 302
#     assert survey.question_set.exists()


# def test_option_create_view(authenticated_client, survey, question):
#     url = reverse("survey_option_create", args=[survey.pk, question.pk])
#     response = authenticated_client.post(url, {"text": "Yes"})
#     assert response.status_code == 200
#     assert question.option_set.exists()


# def test_active_survey_list_view(authenticated_client, survey):
#     survey.is_active = True
#     survey.save()
#     response = authenticated_client.get(reverse("active_survey"))
#     assert response.status_code == 200
#     assert survey.title in response.content.decode()


# def test_start_survey_view_get(authenticated_client, survey):
#     survey.is_active = True
#     survey.save()
#     response = authenticated_client.get(reverse("survey_start", args=[survey.pk]))
#     assert response.status_code == 200


# def test_start_survey_view_post(authenticated_client, survey):
#     survey.is_active = True
#     survey.save()
#     response = authenticated_client.post(reverse("survey_start", args=[survey.pk]))
#     assert response.status_code == 302
#     assert Response.objects.filter(survey=survey).exists()


# def test_survey_report_view(authenticated_client, survey, question, option):
#     survey.is_active = True
#     survey.save()
#     url = reverse("survey_report", args=[survey.pk])
#     response = authenticated_client.get(url)
#     assert response.status_code == 200
#     assert question.text in response.content.decode()


# def test_survey_response_view_get(authenticated_client, survey, question, option):
#     survey.is_active = True
#     survey.save()
#     response_obj = Response.objects.create(survey=survey, is_complete=False)
#     url = reverse("survey_response", args=[survey.pk, response_obj.pk])
#     response = authenticated_client.get(url)
#     assert response.status_code == 200
#     assert question.text in response.content.decode()
