# Generated by Django 3.1.3 on 2020-12-25 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20201225_0304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courses',
            old_name='slug',
            new_name='course_slug',
        ),
    ]
