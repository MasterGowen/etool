from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


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

    sex = models.CharField("Пол", max_length=1, choices=SEXES, default='U')
    department = models.CharField('Институт', max_length=1024, blank=True, null=True)
    group_number = models.CharField('Номер группы', max_length=1024, blank=True, null=True)
    institute = models.CharField('Университет', max_length=1024, blank=True, null=True)
    checked = models.BooleanField("Персона проверена", default=False)

    class Meta:
        verbose_name = 'персона'
        verbose_name_plural = 'персоны'

    def get_person_projects(self):
        registrations = ProjectUserRegistration.objects.filter(person=self)
        projects = [r.project for r in registrations]
        return projects if projects else []

    def is_full(self):
        return all([
            self.first_name != "",
            self.last_name != ""
        ])

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

    def count_open(self):
        count = 0
        for d in Diagnostic.objects.filter(published="p"):
            if not d.has_answer(self) and d.status == "open":
                count += 1
        return count


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
    role = models.CharField("Роль", max_length=8, choices=ROLES)

    class Meta:
        unique_together = ('person', 'event',)

    def __str__(self):
        return " ".join([str(self.person), str(self.event), str(self.role)])


class ProjectUserRegistration(models.Model):
    class Meta:
        verbose_name = 'регистрация пользователя на событие'
        verbose_name_plural = 'регистрации пользователей на события'

    ROLES = (
        ("student", "Студент"),
        ("staff", "Преподаватель"),
        ("admin", "Администратор"),
    )

    person = models.ForeignKey("Person", verbose_name="Персона", on_delete=models.CASCADE)
    project = models.ForeignKey("Project", verbose_name="Событие", on_delete=models.CASCADE)
    role = models.CharField("Тип регистрации", max_length=8, choices=ROLES)

    class Meta:
        unique_together = ('person', 'project',)

    def __str__(self):
        return f"<{self.person} - {self.project.title} - {self.role}>"


class ProjectImage(models.Model):
    image = models.FileField(upload_to="images/%Y/%m/%d")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name='images')


class EventImage(models.Model):
    image = models.FileField(upload_to="images/%Y/%m/%d")
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='images')


class ProjectFile(models.Model):
    file = models.FileField(upload_to="files/%Y/%m/%d")
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name='files')


class EventFile(models.Model):
    file = models.FileField(upload_to="files/%Y/%m/%d")
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='files')


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

    events = models.ManyToManyField("Event", blank=True)

    class Meta:
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'

    def get_students(self):
        registrations = [s.person for s in EventUserRegistration.objects.filter(event__in=self.events.all(), role="student")]
        return list(registrations)

    def get_staff(self):
        registrations = [s.person for s in EventUserRegistration.objects.filter(event__in=self.events.all(), role="staff")]
        registrations += [s.person for s in ProjectUserRegistration.objects.filter(project=self, role="staff")]
        return list(registrations)

    def get_images(self):
        return ProjectImage.objects.filter(project=self)


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

    subevents = models.ManyToManyField("Subevent", blank=True)

    def get_students(self):
        registrations = [s.person for s in EventUserRegistration.objects.filter(event=self, role="student")]
        return list(registrations)

    def get_staff(self):
        registrations = [s.person for s in EventUserRegistration.objects.filter(event=self, role="staff")]
        return list(registrations)

    def get_images(self):
        return EventImage.objects.filter(event=self)

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'события'


class Diagnostic(models.Model):
    STATUSES = (
        ('h', "Скрыт"),
        ('p', "Опубликован"),
    )
    TYPES = (("h", "html"), ("j", "json"))
    title = models.CharField("Название диагностики", max_length=1024, blank=False)
    description = models.TextField("Описание диагностики", blank=True, default="")
    short_description = models.TextField("Краткое описание диагностики", blank=True, default="")
    type = models.CharField("Тип", choices=TYPES, max_length=1, default="h")
    image = models.ImageField("Изображение", blank=True, null=True)
    html = models.TextField("Отображение", blank=True, null=True)
    json = models.TextField("json", blank=True, null=True)
    check_func = models.TextField("Функция проверки", blank=True, null=True)
    render = models.TextField("Функция отрисовки", blank=True, null=True)
    weight = models.IntegerField("Вес", default=0, blank=False, null=False)
    startdate = models.DateTimeField("Дата начала", blank=True, null=True)
    enddate = models.DateTimeField("Дата завершения", blank=True, null=True)
    published = models.CharField("Статус публикации", max_length=1, choices=STATUSES, default='h')

    class Meta:
        verbose_name = 'диагностика'
        verbose_name_plural = 'диагностики'

    def has_answer(self, person):
        return StudentDiag.objects.filter(diagnostic=self, person=person).exists()

    @property
    def status(self):
        if self.enddate:
            if self.enddate > timezone.now() > self.startdate:
                return "open"
            else:
                return "close"
        else:
            if timezone.now() > self.startdate:
                return "open"
            else:
                return "close"


class StudentDiag(models.Model):
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE, )
    person = models.ForeignKey(Person, on_delete=models.CASCADE, )
    answer = models.TextField("Ответ студента", null=True, blank=True)
    analisys = models.TextField("Анализ диагностики", null=True, blank=True)
