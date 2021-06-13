from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название компании')
    location = models.CharField(max_length=64, verbose_name='География')
    logo = models.ImageField(upload_to=settings.MEDIA_COMPANY_IMAGE_DIR, verbose_name='Логотип')
    description = models.TextField(verbose_name='Информация о компании')
    employee_count = models.IntegerField(verbose_name='Количество человек в компании')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='company_owner',
                                 verbose_name='Владелец')

    def __str__(self):
        return f'Компания {self.name}'

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Specialty(models.Model):
    code = models.CharField(max_length=64, verbose_name='Код специальности')
    title = models.CharField(max_length=64, verbose_name='Специальность')
    picture = models.ImageField(upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'


class Vacancy(models.Model):
    title = models.CharField(max_length=64, verbose_name='Наименование вакансии')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies',
                                  verbose_name='Специальность')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies', verbose_name='Компания')
    skills = models.CharField(max_length=256, verbose_name='Навыки')
    description = models.TextField(verbose_name='Описание вакансии')
    salary_min = models.IntegerField(verbose_name='Зарплата от')
    salary_max = models.IntegerField(verbose_name='До')
    published_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')

    def __str__(self):
        return f'{self.title} id = {self.pk}'

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class Application(models.Model):
    written_username = models.CharField(max_length=32, verbose_name='Отклик от:')
    written_phone = models.IntegerField(verbose_name='Номер телефона')
    written_cover_letter = models.TextField(verbose_name='Сопроводительное письмо')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications', verbose_name='Вакансия')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name='Пользователь')

    def __str__(self):
        return self.written_username

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
