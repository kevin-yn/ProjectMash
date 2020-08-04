from .models import Projects, Comparison_Pair
from django.db import connection
# get all the projects current in the database, generate all possible pairs and insert into Comparison_Pair
def generate():
    # drop all records
    with connection.cursor() as cursor:
        cursor.execute(
            'DELETE FROM projects_comparison_pair'
        )

    # get all projects_id
    projects = Projects.objects.raw(
        'SELECT id FROM projects_projects;'
    )
    size = len(list(projects))

    for i in range(0, size):
        for j in range(i + 1, size):
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO projects_comparison_pair (projectA_id, projectB_id, count) VALUES (%s, %s, %s)',
                    [projects[i].id, projects[j].id, 0]
                )
