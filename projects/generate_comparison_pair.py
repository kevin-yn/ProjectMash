from .models import Projects, Comparison_Pair
from django.db import connection
# get all the projects current in the database, generate all possible pairs and insert into Comparison_Pair
def generate(id):
    # get all projects_id
    projects = Projects.objects.raw(
        'SELECT id FROM projects_projects WHERE id != %s', [id]
    )

    for p in projects:
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO projects_comparison_pair (projectA_id, projectB_id, count) VALUES (%s, %s, %s)',
                [id, p.id, 0]
            )
