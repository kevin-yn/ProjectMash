from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    # index page: display all projects
    path('', views.index, name='index'),
    # detail page: display more information of one project
    path('<int:_id>/', views.detail, name='detail'),
    # create page: display the form to create new project
    path('create/', views.display_create_page, name='create'),
    # edit page: display the form to edit a existing project
    path('<int:_id>/edit', views.edit, name = 'edit'),
    # delete the project, redirect to index page
    path('<int:_id>/delete', views.delete, name='delete'),
    # display the search page
    path('search_form', views.display_search_page, name = 'search_form'),
    # search route
    path('search', views.search, name='search'),
    # generate all possible pairs from current list of projects
    path('generate', views.generate_view, name='generate_view'),
    path('vote/', views.display_vote_page, name='vote'),
    path('vote_process/<int:_id>', views.vote_process, name = 'vote_process'),
]
