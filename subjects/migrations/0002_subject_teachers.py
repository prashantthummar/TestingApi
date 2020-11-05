# Generated by Django 3.1.2 on 2020-11-05 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teachers', '0001_initial'),
        ('subjects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='teachers',
            field=models.ManyToManyField(blank=True, related_name='subject_teachers', to='teachers.Teacher'),
        ),
    ]
