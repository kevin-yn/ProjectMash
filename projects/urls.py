from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.index, name='index'), # index page: display all projects
    path('<int:_id>/', views.detail, name='detail'), # detail page: display more information of one project
    path('create/', views.create, name='create'), # create page: display the form to create new project
    path('<int:_id>/edit', views.edit, name = 'edit'), # edit page: display the form to edit a existing project
    path('<int:_id>/delete', views.delete, name='delete'), # delete the project, redirect to index page
]
