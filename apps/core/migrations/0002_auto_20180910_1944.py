# Generated by Django 2.1 on 2018-09-10 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnostic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024, verbose_name='Название диагностики')),
                ('html', models.TextField(blank=True, null=True, verbose_name='Отображение')),
                ('check_func', models.TextField(blank=True, null=True, verbose_name='Функция проверки')),
            ],
            options={
                'verbose_name': 'диагностика',
                'verbose_name_plural': 'диагностики',
            },
        ),
        migrations.CreateModel(
            name='StudentDiag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True, null=True, verbose_name='Ответ студента')),
                ('analisys', models.TextField(blank=True, null=True, verbose_name='Анализ диагностики')),
                ('diagnostic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Diagnostic')),
            ],
        ),
        migrations.AlterField(
            model_name='person',
            name='department',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Институт'),
        ),
        migrations.AlterField(
            model_name='person',
            name='institute',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Университет'),
        ),
        migrations.AlterField(
            model_name='person',
            name='sex',
            field=models.CharField(choices=[('U', 'Не выбран'), ('F', 'Женский'), ('M', 'Мужской')], default='U', max_length=1, verbose_name='Пол'),
        ),
        migrations.AddField(
            model_name='studentdiag',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Person'),
        ),
    ]
