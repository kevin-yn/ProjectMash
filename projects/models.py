import datetime
from django.db import models
from django.utils import timezone

class Projects(models.Model):
    project_name = models.CharField(max_length=30)
    project_summary = models.CharField(max_length=200)
    project_link = models.CharField(max_length=200)
    project_backendLanguage = models.CharField(max_length=30)
    def __str__(self):
        return self.project_name
    

class Comparison_Pair(models.Model):
    projectA = models.ForeignKey(
        Projects, on_delete=models.CASCADE, related_name='ComparedAsA')
    projectB = models.ForeignKey(
        Projects, on_delete=models.CASCADE, related_name='ComparedAsB')
    count = models.IntegerField()

    def __str__(self):
        return projectA + " : " + projectB
