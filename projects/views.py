from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Projects
from django.db import connection

def index(request):
    if request.method == 'GET':
        latest_project_list = Projects.objects.raw(
            'SELECT* FROM projects_projects')
        # latest_project_list = Projects.objects.order_by('-pub_date')[:5]
        template = loader.get_template('projects/index.html')
        context = {
            'latest_project_list': latest_project_list
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        project_name = request.POST.get('project_name', 'nothing')
        project_link = request.POST.get('project_link', 'nothing')
        
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO projects_projects (project_name, project_link) VALUES (%s, %s)", [
                           project_name, project_link])
            row = cursor.fetchone()
            print(row)
        return HttpResponseRedirect(reverse('projects:index'))

def detail(request, _id):
    if request.method == 'GET': # detail page
        project = Projects.objects.raw('SELECT* FROM projects_projects WHERE id = %s', [_id])
        return render(request, 'projects/detail.html', {'project': project[0]})
    elif request.method == 'POST': # edit current project
        project_name = request.POST.get('project_name', 'nothing')
        project_link = request.POST.get('project_link', 'nothing')
        with connection.cursor() as cursor:
            cursor.execute('UPDATE projects_projects SET project_name = %s, project_link = %s WHERE id = %s', 
                           [project_name, project_link, _id])
            row = cursor.fetchone()
            print(row)
        return HttpResponseRedirect(reverse('projects:detail', args = (_id,)))


def create(request):
    template = loader.get_template('projects/create.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

def edit(request, _id):
    project = Projects.objects.raw(
        'SELECT* FROM projects_projects WHERE id = %s', [_id])
    return render(request, 'projects/edit.html', {'project': project[0]})


def delete(request, _id):
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM projects_projects WHERE id = %s',
                       [_id])
    return HttpResponseRedirect(reverse('projects:index'))

