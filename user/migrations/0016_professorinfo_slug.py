# Generated by Django 3.1.3 on 2020-12-25 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20201225_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='professorinfo',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
