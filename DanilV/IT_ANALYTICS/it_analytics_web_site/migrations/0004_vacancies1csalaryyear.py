# Generated by Django 4.1.5 on 2023-01-14 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('it_analytics_web_site', '0003_allvacanciessalaryyear_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacancies1CSalaryYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Название')),
                ('curren', models.CharField(max_length=128, verbose_name='Валюта')),
                ('year', models.PositiveIntegerField(verbose_name='Год')),
                ('value', models.PositiveIntegerField(verbose_name='Средняя зарплата')),
            ],
            options={
                'verbose_name': 'Строку',
                'verbose_name_plural': 'Динамика зарплат по годам для 1C-разработчика',
            },
        ),
    ]
