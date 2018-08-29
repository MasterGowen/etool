from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField('Имя пользователя', max_length=32, blank=True, default='')
    last_name = models.CharField('Фамилия пользователя', max_length=32, blank=True, default='')
    second_name = models.CharField('Отчество пользователя', max_length=32, blank=True, default='')
    SEXES = (
        ('U', 'Не выбран'),
        ('F', 'Женский'),
        ('M', 'Мужской'),
    )

    sex = models.CharField(max_length=1, choices=SEXES, default='U')
    department = models.CharField('Кафедра/Институт', max_length=1024, blank=True, null=True)
    group_number = models.CharField('Номер группы', max_length=1024, blank=True, null=True)
    institute = models.CharField('Институт/Университет', max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = 'персона'
        verbose_name_plural = 'персоны'

    def __str__(self):
        if self.first_name and self.last_name:
            return ' '.join([str(self.first_name), str(self.last_name)])
        else:
            return str(self.user)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Person.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.person.save()


class Event(models.Model):
    STATUSES = (
        ('h', "Скрыт"),
        ('p', "Опубликован"),
    )
    title = models.CharField("Название события", max_length=256, blank=False)
    description = models.TextField("Описание события", blank=True, default="")
    status = models.CharField("Статус публикации", max_length=1, choices=STATUSES, default='h')
    _startdate = models.DateTimeField("Начало события", blank=True, null=True)
    _enddate = models.DateTimeField("Конец события", blank=True, null=True)

    subevents = models.ManyToManyField("Subevent")

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'события'


class Subevent(models.Model):
    STATUSES = (
        ('h', "Скрыт"),
        ('p', "Опубликован"),
    )

    title = models.CharField("Название события", max_length=256, blank=False)
    description = models.TextField("Описание события", blank=True, default="")
    status = models.CharField("Статус публикации", max_length=1, choices=STATUSES, default='h')
    _startdate = models.DateTimeField("Начало события", blank=True, null=True)
    _enddate = models.DateTimeField("Конец события", blank=True, null=True)


class EventUserRegistration(models.Model):
    class Meta:
        verbose_name = 'регистрация пользователя на событие'
        verbose_name_plural = 'регистрации пользователей на события'

    ROLES = (
        ("student", "Студент"),
        ("staff", "Преподаватель"),
        ("admin", "Администратор"),
    )

    person = models.ForeignKey("Person", verbose_name="Персона", on_delete=models.CASCADE)
    event = models.ForeignKey("Event", verbose_name="Событие", on_delete=models.CASCADE)
    role = models.CharField("Тип регистрации", max_length=8, choices=ROLES)

    class Meta:
        unique_together = ('person', 'event',)

    def __str__(self):
        return " ".join([str(self.person), str(self.event), str(self.role)])


class Project(models.Model):
    STATUSES = (
        ('h', "Скрыт"),
        ('p', "Опубликован"),
    )
    title = models.CharField("Название проекта", max_length=256, blank=False)
    description = models.TextField("Описание проекта", blank=True, default="")
    status = models.CharField("Статус публикации", max_length=1, choices=STATUSES, default='h')
    _startdate = models.DateTimeField("Начало проекта", blank=True, null=True)
    _enddate = models.DateTimeField("Конец проекта", blank=True, null=True)

    events = models.ManyToManyField("Event")

    class Meta:
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'
