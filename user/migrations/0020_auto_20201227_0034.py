# Generated by Django 3.1.3 on 2020-12-26 22:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_auto_20201225_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='course_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='level',
            field=models.CharField(choices=[('First Year', 'First Year'), ('Second Year', 'Second Year'), ('Third Year', 'Third Year'), ('Fourth Year', 'Fourth Year'), ('Fivth Year', 'Fivth Year'), ('Sixth Year', 'Sixth Year')], max_length=25),
        ),
    ]