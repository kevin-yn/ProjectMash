from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from .models import Projects, Comparison_Pair, Score
from django.db import connection
from .generate_comparison_pair import generate
import random
from urllib import parse
from urllib.parse import urlparse
from projects.elo_rating import elo_rating

def index(request):
    if request.method == 'GET':
        latest_project_list = Projects.objects.raw(
            'SELECT* FROM projects_projects')
        # latest_project_list = Projects.objects.order_by('-pub_date')[:5]
        template = loader.get_template('projects/index.html')
        context = {
            'num': len(list(latest_project_list)),
            'latest_project_list': latest_project_list
        }
        return HttpResponse(template.render(context, request))
    elif request.method == 'POST':
        project_name = request.POST.get('project_name', 'nothing')
        project_summary = request.POST.get('project_summary', 'nothing')
        project_backendLanguage = request.POST.get(
            'project_backendLanguage', 'nothing')
        project_link = request.POST.get('project_link', 'nothing')
        url_parsed = parse.urlparse(project_link)
        qsl = parse.parse_qs(url_parsed.query)
        host = '{uri.scheme}://{uri.netloc}/'.format(uri=url_parsed)
        if (host == "https://www.youtube.com/"):
            project_link = "https://www.youtube.com/embed/"+qsl['v'][0]+"?controls=1"
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO projects_projects (project_name, project_backendLanguage, project_summary, project_link) VALUES (%s, %s, %s, %s)", [
                           project_name, project_backendLanguage, project_summary, project_link])
            # insert into score tabel for this project
            cursor.execute('SELECT id FROM projects_projects WHERE id NOT IN(SELECT project_id FROM projects_score) LIMIT 1')
            id = cursor.fetchone()[0]
            # generate score
            cursor.execute(
                "INSERT INTO projects_score(project_id, score, first_criterion_score, second_criterion_score, third_criterion_score) VALUES(%s, 1400, 0, 0, 0)", [id])
            # generate pair
            generate(id)


        return HttpResponseRedirect(reverse('projects:index'))

def detail(request, _id):
    if request.method == 'GET': # detail page
        project = Projects.objects.raw('SELECT* FROM projects_projects WHERE id = %s', [_id])
        return render(request, 'projects/detail.html', {'project': project[0]})
    elif request.method == 'POST': # edit current project
        project_name = request.POST.get('project_name', 'nothing')
        project_summary = request.POST.get('project_summary', 'nothing')
        project_backendLanguage = request.POST.get(
            'project_backendLanguage', 'nothing')
        project_link = request.POST.get('project_link', 'nothing')
        # url_parsed = parse.urlparse(project_link)
        # qsl = parse.parse_qs(url_parsed.query)
        # host = '{uri.scheme}://{uri.netloc}/'.format(uri=url_parsed)
        # if (host == "https://www.youtube.com/"):
        #     project_link = "https://www.youtube.com/embed/" + \
        #         qsl['v'][0]+"?controls=1"
        with connection.cursor() as cursor:
            cursor.execute('UPDATE projects_projects SET project_name = %s, project_link = %s, project_summary = %s, project_backendLanguage = %s WHERE id = %s',
                           [project_name, project_link, project_summary, project_backendLanguage, _id])
            row = cursor.fetchone()
            print(row)
        return HttpResponseRedirect(reverse('projects:detail', args = (_id,)))

def display_create_page(request):
    template = loader.get_template('projects/create.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

def edit(request, _id):
    project = Projects.objects.raw(
        'SELECT* FROM projects_projects WHERE id = %s', [_id])
    return render(request, 'projects/edit.html', {'project': project[0]})

def delete(request, _id):
    # with connection.cursor() as cursor:
    #     cursor.execute('DELETE FROM projects_projects WHERE id = %s',
    #                    [_id])
    Projects.objects.filter(id=_id).delete()
    return HttpResponseRedirect(reverse('projects:index'))

def search(request):
    project_name = request.GET.get('project_name', 'nothing')
    language = request.GET.get('backendLanguage', 'nothing')
    print("-------")
    print(language)
    if project_name != '':
        projects = Projects.objects.raw(
            'SELECT* FROM projects_projects WHERE project_name = %s', [project_name])
    elif language != '':
        print("haha---------")
        projects = Projects.objects.raw(
            'SELECT* FROM projects_projects WHERE project_backendLanguage = %s', [language])
    else:
        return HttpResponse("no input detected")
    if len(list(projects)) > 0 :
        context = {
            'num': len(list(projects)),
            'latest_project_list': projects
        }
        template = loader.get_template('projects/index.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("no project found")

def search_lan(request):
    language = request.GET.get('backendLanguage', 'nothing')
    if(language == ''):
        return HttpResponse("no input detected")
    with connection.cursor() as cursor:
        cursor.execute(
        'SELECT projects_projects.project_backendLanguage, AVG(projects_score.score) AS avg_score FROM(projects_projects JOIN projects_score ON projects_projects.id=projects_score.project_id) GROUP BY projects_projects.project_backendLanguage HAVING projects_projects.project_backendLanguage = %s'        ,[language])
        results = cursor.fetchall()
        print(results[0][0])
    if(len(list(results)) == 0):
        print("000000000")
        return HttpResponse("no such language used")
    else:
        template = loader.get_template('projects/lanScoreBoard.html')
        context = {
            'lan': results[0][0],
            'score': results[0][1]
        }
        return HttpResponse(template.render(context, request))

def display_search_page(request):
    template = loader.get_template('projects/search.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

def display_vote_page(request):
    
    # from the list of pair, randomly select one pair
    comparison_pairs = Comparison_Pair.objects.raw(
        'SELECT * FROM projects_comparison_pair WHERE count = (SELECT MIN(count) FROM projects_comparison_pair)')
    if(len(list(comparison_pairs))) == 0:
        return HttpResponseRedirect(reverse('projects:index'))
    template = loader.get_template('projects/vote.html')
    context = {
        'comparison_pair' : comparison_pairs[random.randint(0, len(list(comparison_pairs)) - 1)],
    }
    # find the Comparison Pair that has the least count

    return HttpResponse(template.render(context, request))

def vote_process(request, _id):
    # use the id get the comparison_pair
    comparison_pair = Comparison_Pair.objects.raw(
        'SELECT * FROM projects_comparison_pair WHERE id = %s', [_id,])[0]
    scoreAObject = Score.objects.raw(
        'SELECT * FROM projects_score WHERE project_id = %s', [comparison_pair.projectA.id]
    )[0]
    scoreBObject = Score.objects.raw(
        'SELECT * FROM projects_score WHERE project_id = %s', [
            comparison_pair.projectB.id]
    )[0]
    data = request.POST.copy()
    criterion = data.get('criterion', 'default')
    choice = data.get('choice')
    actual = 1 # used for the elo rating function
    # update the count
    newCount = comparison_pair.count + 1
    with connection.cursor() as cursor:
        cursor.execute('UPDATE projects_comparison_pair SET count = %s WHERE id = %s', [
            newCount, comparison_pair.id])
    
    # update the Score
    if(choice == 'rB'):
        actual = 0
    updatedScores = elo_rating(scoreAObject.score, scoreBObject.score, 30, actual)

    with connection.cursor() as cursor:
        cursor.execute('UPDATE projects_score SET score = %s WHERE project_id = %s', [
                        updatedScores[0], scoreAObject.project_id])
        cursor.execute('UPDATE projects_score SET score = %s WHERE project_id = %s', [
                       updatedScores[1], scoreBObject.project_id])
    # update the feedBack only when necessary
    if(criterion != 'default'):
        if(criterion == '1'):
            newScoreA = scoreAObject.first_criterion_score + 1
            if(0 == actual):
                newScoreA = scoreAObject.first_criterion_score - 1
            with connection.cursor() as cursor:
                cursor.execute('UPDATE projects_score SET first_criterion_score = %s WHERE project_id = %s', [
                    newScoreA, scoreAObject.project_id])

            newScoreB = scoreBObject.first_criterion_score + 1
            if(1 == actual):
                newScoreB = scoreBObject.first_criterion_score - 1
            with connection.cursor() as cursor:
                cursor.execute('UPDATE projects_score SET first_criterion_score = %s WHERE project_id = %s', [
                    newScoreB, scoreBObject.project_id])
        elif(criterion == '2'):
            newScoreA = scoreAObject.second_criterion_score + 1
            if(0 == actual):
                newScoreA = scoreAObject.second_criterion_score - 1
            with connection.cursor() as cursor:
                cursor.execute('UPDATE projects_score SET second_criterion_score = %s WHERE project_id = %s', [
                    newScoreA, scoreAObject.project_id])

            newScoreB = scoreBObject.second_criterion_score + 1
            if(1 == actual):
                newScoreB = scoreBObject.second_criterion_score - 1
            with connection.cursor() as cursor:
                cursor.execute('UPDATE projects_score SET second_criterion_score = %s WHERE project_id = %s', [
                    newScoreB, scoreBObject.project_id])
        elif(criterion == '3'):
            newScoreA = scoreAObject.third_criterion_score + 1
            if(0 == actual):
                newScoreA = scoreAObject.third_criterion_score - 1
            with connection.cursor() as cursor:
                cursor.execute('UPDATE projects_score SET third_criterion_score = %s WHERE project_id = %s', [
                    newScoreA, scoreAObject.project_id])

            newScoreB = scoreBObject.third_criterion_score + 1
            if(1 == actual):
                newScoreB = scoreBObject.third_criterion_score - 1
            with connection.cursor() as cursor:
                cursor.execute('UPDATE projects_score SET third_criterion_score = %s WHERE project_id = %s', [
                    newScoreB, scoreBObject.project_id])

    return HttpResponseRedirect(reverse('projects:scoreBoard'))





    template = loader.get_template('projects/vote_process.html')
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         'SELECT* FROM (projects_projects JOIN projects_score ON projects_score.project_id = projects_projects.id)')
    #     projects = cursor.fetchone()
    projects = Projects.objects.raw(
        'SELECT* FROM (projects_projects JOIN projects_score ON projects_score.project_id = projects_projects.id)')
    context = {
        'projects' : projects,
    }
    return HttpResponse(template.render(context, request))

def scoreBoard(request):
    template = loader.get_template('projects/scoreBoard.html')
    allProjects = Score.objects.raw(
        'SELECT* FROM (projects_projects JOIN projects_score ON projects_score.project_id = projects_projects.id) ORDER BY projects_score.score  DESC LIMIT 5 ')
    # print(projects)
    context = {
        'allProjects' : allProjects,
    }
    return HttpResponse(template.render(context, request))

def feedback(request, _id):
    threshold = 1
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT* FROM (projects_projects JOIN projects_score ON projects_score.project_id = projects_projects.id) WHERE id = %s', [_id])
        project = cursor.fetchone()
    allScores = Score.objects.raw('SELECT project_id FROM projects_score ORDER BY score DESC')
    rank = 1
    for x in allScores:
        if(project[0] == x.project_id):
            break
        else:
            rank = rank + 1
    return render(request, 'projects/feedback.html', {
        'project_name': project[1],
        'score': project[5],
        'firstScore': project[7],
        'secondScore': project[8],
        'thirdScore': project[9],
        'hthreshold': threshold,
        'lthreshold': threshold * -1,
        'rank': rank,
        'totalnum': len(list(allScores))}
        )
