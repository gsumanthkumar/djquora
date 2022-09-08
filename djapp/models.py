from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    description = models.CharField(max_length=255,default=None)
    asked_by = models.ForeignKey(User,on_delete=models.CASCADE)
    asked_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    description = models.TextField()
    answered_by = models.ForeignKey(User,on_delete=models.CASCADE)
    answered_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Answervote(models.Model):
    answer = models.ForeignKey(Answer,on_delete=models.CASCADE)
    vote = models.IntegerField()
    voted_by = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)