# Generated by Django 3.1.2 on 2020-11-05 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('join_id', models.CharField(blank=True, max_length=32, null=True)),
                ('department_id', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('contact_phone', models.CharField(blank=True, max_length=32, null=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('accepting_req', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
