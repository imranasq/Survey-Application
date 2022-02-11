from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Survey


# Create your views here.
@login_required
def survey_list(request):
    """User can view all their surveys"""
    surveys = Survey.objects.filter(creator=request.user).order_by("-created_at").all()
    return render(request, "survey-list.html", {"surveys": surveys})