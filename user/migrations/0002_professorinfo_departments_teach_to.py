# Generated by Django 3.1.3 on 2020-12-14 23:02

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='professorinfo',
            name='departments_teach_to',
            field=multiselectfield.db.fields.MultiSelectField(choices=[], default=1, max_length=200),
            preserve_default=False,
        ),
    ]
