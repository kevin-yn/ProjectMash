from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Projects

def index(request):
    latest_project_list = Projects.objects.order_by('-pub_date')[:5]
    template = loader.get_template('projects/index.html')
    context = {
        'latest_project_list': latest_project_list
    }
    return HttpResponse(template.render(context, request))

def detail(request, _id):
    project = get_object_or_404(Projects, pk=_id)
    return render(request, 'projects/detail.html', {'project': project})
