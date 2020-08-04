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
    countA = models.IntegerField(default=0)
    countB = models.IntegerField(default=0)
    #reason 1 A win: because of its difficulty
    r1Aw = models.IntegerField(default=0)
    r1Bw = models.IntegerField(default=0)
    #reason 2 A win: because of its creativity
    r2Aw = models.IntegerField(default=0)
    r2Bw = models.IntegerField(default=0)

    def __str__(self):
        return projectA + " : " + projectB

# class Choice(models.Model):
#     pair = models.ForeignKey(Comparison_Pair, on_delete=models.CASCADE)
#     choiceA = pair.projectA.project_name + " is better."
#     choiceB = pair.projectB.project_name + " is better."

class Score(models.Model):
    project = models.ForeignKey(Projects, on_delete = models.CASCADE)
    score = models.IntegerField(default=0)
