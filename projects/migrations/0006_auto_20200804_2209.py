# Generated by Django 3.0.8 on 2020-08-04 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20200804_2134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comparison_pair',
            name='countA',
        ),
        migrations.RemoveField(
            model_name='comparison_pair',
            name='countB',
        ),
        migrations.RemoveField(
            model_name='comparison_pair',
            name='r1Aw',
        ),
        migrations.RemoveField(
            model_name='comparison_pair',
            name='r1Bw',
        ),
        migrations.RemoveField(
            model_name='comparison_pair',
            name='r2Aw',
        ),
        migrations.RemoveField(
            model_name='comparison_pair',
            name='r2Bw',
        ),
    ]
