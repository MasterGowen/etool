# Generated by Django 2.1 on 2018-10-11 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_person_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdiag',
            name='is_checked',
            field=models.BooleanField(default=False, verbose_name='Проверена'),
        ),
        migrations.AddField(
            model_name='studentdiag',
            name='result',
            field=models.TextField(blank=True, null=True, verbose_name='Результат диагностики'),
        ),
    ]
