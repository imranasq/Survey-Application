from django.db import models
from user.models import User

# Create your models here.

class Survey(models.Model):
    title = models.CharField(max_length=255, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    response_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="responder", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Question(models.Model):
    title = models.CharField(max_length=255, null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    Answer=models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=128)
    def __str__(self):
        return self.text

class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)
    # completed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
