import pytest
from django.urls import reverse
from .models import Survey, Question, Option, Response, Answer
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="#1Testpass",
        is_active=True
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    response = client.post("/api/token/", {
        "email": user.email,
        "password": "#1Testpass"
    }, format="json")

    assert response.status_code == 200, f"Token request failed: {response.content}"
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def survey(user):
    return Survey.objects.create(title="Test Survey", creator=user)

@pytest.fixture
def question(survey):
    return Question.objects.create(title="Sample Question", survey=survey)

@pytest.fixture
def option(question):
    return Option.objects.create(text="Option 1", question=question)

@pytest.mark.django_db
def test_survey_list_view_redirects_for_anonymous(client):
    response = client.get(reverse("survey_list"))
    assert response.status_code == 302
    assert "/login/" in response.url

@pytest.mark.django_db
def test_survey_list_view(authenticated_client):
    response = authenticated_client.get(reverse("survey_list"))
    assert response.status_code == 302

@pytest.mark.django_db
def test_survey_create_view(authenticated_client):
    response = authenticated_client.post(reverse("create_survey"), {"title": "New Survey"})
    assert response.status_code == 302  # Redirect after success

@pytest.mark.django_db
def test_survey_edit_view(authenticated_client, survey):
    response = authenticated_client.get(reverse("survey_edit", args=[survey.pk]))
    assert response.status_code == 302

@pytest.mark.django_db
def test_survey_delete_view(authenticated_client, survey):
    response = authenticated_client.post(reverse("survey_delete", args=[survey.pk]))
    assert response.status_code == 302
    assert not Survey.objects.filter(pk=survey.pk).exists()

@pytest.mark.django_db
def test_question_create_view(authenticated_client, survey):
    url = reverse("survey_question_create", args=[survey.pk])
    import pdb
    pdb.set_trace()
    response = authenticated_client.post(url, {"title": "What is your name?"})
    print(response.content)
    assert response.status_code == 302
    assert survey.question_set.exists()

@pytest.mark.django_db
def test_option_create_view(authenticated_client, survey, question):
    url = reverse("survey_option_create", args=[survey.pk, question.pk])
    response = authenticated_client.post(url, {"title": "Yes"})
    assert response.status_code == 200
    assert question.option_set.exists()

@pytest.mark.django_db
def test_active_survey_list_view(authenticated_client, survey):
    survey.is_active = True
    survey.save()
    response = authenticated_client.get(reverse("active_survey"))
    assert response.status_code == 200
    assert survey.title in response.content.decode()

@pytest.mark.django_db
def test_start_survey_view_get(authenticated_client, survey):
    survey.is_active = True
    survey.save()
    response = authenticated_client.get(reverse("survey_start", args=[survey.pk]))
    assert response.status_code == 200


@pytest.mark.django_db
def test_start_survey_view_post(authenticated_client, survey):
    survey.is_active = True
    survey.save()
    response = authenticated_client.post(reverse("survey_start", args=[survey.pk]))
    assert response.status_code == 302
    assert Response.objects.filter(survey=survey).exists()

@pytest.mark.django_db
def test_survey_report_view(authenticated_client, survey, question, option):
    survey.is_active = True
    survey.save()
    url = reverse("survey_report", args=[survey.pk])
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert question.title in response.content.decode()

@pytest.mark.django_db
def test_survey_response_view_get(authenticated_client, survey, question, option):
    survey.is_active = True
    survey.save()
    response_obj = Response.objects.create(survey=survey, is_complete=False)
    url = reverse("survey_response", args=[survey.pk, response_obj.pk])
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert question.title in response.content.decode()
