import datetime
from django.db import models
from django.utils import timezone

class Projects(models.Model):
    project_name = models.CharField(max_length=200)
    project_link = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.project_name
    