# Generated by Django 4.1.5 on 2023-01-13 17:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('it_analytics_web_site', '0002_allvacanciessalaryyear'),
    ]

    operations = [
        migrations.AddField(
            model_name='allvacanciessalaryyear',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=128, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='allvacanciessalaryyear',
            name='curren',
            field=models.CharField(max_length=128, verbose_name='Валюта'),
        ),
    ]